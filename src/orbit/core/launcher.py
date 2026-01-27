"""Mission launcher - executes AppleScript for satellites."""

import subprocess
from typing import Optional, Any

try:
    from jinja2 import Template
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

from orbit.core.satellite import Satellite
from orbit.core.shield import SafetyShield
from orbit.core.exceptions import (
    AppleScriptError,
    TemplateRenderingError,
)


class Launcher:
    """Mission launcher - executes AppleScript for satellites."""

    def __init__(
        self,
        safety_shield: Optional["SafetyShield"] = None,
        timeout: int = 30,
        retry_on_failure: bool = False,
        max_retries: int = 3,
    ):
        """Initialize the launcher.

        Args:
            safety_shield: Optional safety shield
            timeout: Script execution timeout in seconds
            retry_on_failure: Whether to retry on failure
            max_retries: Maximum retry attempts
        """
        self.safety_shield = safety_shield
        self.timeout = timeout
        self.retry_on_failure = retry_on_failure
        self.max_retries = max_retries

    def launch(
        self, satellite: Satellite, parameters: dict, bypass_shield: bool = False
    ) -> Any:
        """Launch a mission (execute a satellite).

        Args:
            satellite: The satellite to launch
            parameters: Mission parameters
            bypass_shield: Skip safety checks (not recommended)

        Returns:
            Mission result

        Raises:
            ShieldError: If safety check fails
            AppleScriptError: If execution fails
        """
        # Validate parameters
        satellite.validate_parameters(parameters)

        # Safety check
        if not bypass_shield and self.safety_shield:
            self.safety_shield.validate(satellite, parameters)

        # Render AppleScript template
        script = self._render_template(satellite.applescript_template, parameters)

        # Execute with retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                result = self._execute_applescript(script)
                break
            except AppleScriptError as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    raise
                if not self.retry_on_failure:
                    raise
        else:
            if last_error:
                raise last_error

        # Parse result
        if satellite.result_parser:
            return satellite.result_parser.parse(result) if hasattr(
                satellite.result_parser, "parse"
            ) else satellite.result_parser(result)
        return result

    def _render_template(self, template: str, parameters: dict) -> str:
        """Render AppleScript template using Jinja2.

        Args:
            template: Template string
            parameters: Template parameters

        Returns:
            Rendered script

        Raises:
            TemplateRenderingError: If rendering fails
        """
        if not HAS_JINJA2:
            # Fallback to simple string formatting
            try:
                return template.format(**parameters)
            except KeyError as e:
                raise TemplateRenderingError(f"Missing parameter: {e}")
            except Exception as e:
                raise TemplateRenderingError(f"Template rendering failed: {e}")

        try:
            jinja_template = Template(template)
            return jinja_template.render(**parameters)
        except Exception as e:
            raise TemplateRenderingError(f"Template rendering failed: {e}")

    def _execute_applescript(self, script: str) -> str:
        """Execute AppleScript via osascript.

        Args:
            script: AppleScript to execute

        Returns:
            Script output

        Raises:
            AppleScriptError: If execution fails
        """
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                # Try to provide helpful permission hints
                from orbit.core.permissions import format_error_with_hint
                enhanced_error = format_error_with_hint(error_msg, satellite.name)

                # If we got an enhanced error, use it; otherwise use standard error
                if enhanced_error != f"❌ Error: {error_msg}":
                    raise AppleScriptError(
                        enhanced_error.strip(),
                        script=script,
                        return_code=result.returncode,
                    )
                else:
                    raise AppleScriptError(
                        f"AppleScript execution failed: {error_msg}",
                        script=script,
                        return_code=result.returncode,
                    )

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            raise AppleScriptError(
                f"Script execution timed out after {self.timeout}s"
            )
        except Exception as e:
            raise AppleScriptError(f"Unexpected error: {str(e)}")

    async def launch_async(self, satellite: Satellite, parameters: dict) -> Any:
        """Launch a mission asynchronously.

        Args:
            satellite: The satellite to launch
            parameters: Mission parameters

        Returns:
            Mission result
        """
        import asyncio

        return await asyncio.to_thread(self.launch, satellite, parameters)
