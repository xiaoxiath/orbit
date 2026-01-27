#!/bin/bash
set -e

echo "🚀 Orbit PyPI Package Publishing Script"
echo "========================================"
echo ""

# 检查是否安装了必要的工具
echo "🔍 Checking requirements..."

if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed"
    echo ""
    echo "Install Poetry:"
    echo "  curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    exit 1
fi

if ! command -v twine &> /dev/null; then
    echo "⚠️  Twine is not installed. Installing..."
    pip install twine
fi

echo "✅ All requirements met"
echo ""

# 检查版本号
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📦 Current version: $VERSION"
echo ""

# 确认发布
read -p "📤 Do you want to publish version $VERSION to PyPI? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "🔨 Building package..."

# 清理旧的构建文件
echo "🧹 Cleaning old build files..."
rm -rf dist/ build/ *.egg-info

# 使用 Poetry 构建
poetry build

echo ""
echo "✅ Build complete!"
echo ""

# 显示将要上传的文件
echo "📄 Files to be uploaded:"
ls -lh dist/
echo ""

# 检查包
echo "🔍 Checking package with twine..."
twine check dist/*
echo ""

# 选择发布目标
echo "📌 Choose publish destination:"
echo "  1) TestPyPI (for testing)"
echo "  2) PyPI (production)"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "📤 Publishing to TestPyPI..."
        echo ""
        echo "⚠️  Make sure you have TestPyPI credentials:"
        echo "   https://test.pypi.org/account/register/"
        echo ""
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ Published to TestPyPI!"
        echo ""
        echo "Install with:"
        echo "  pip install --index-url https://test.pypi.org/simple/ orbit-macos"
        ;;
    2)
        echo ""
        echo "📤 Publishing to PyPI..."
        echo ""
        echo "⚠️  Make sure you have PyPI credentials:"
        echo "   https://pypi.org/account/register/"
        echo ""
        twine upload dist/*
        echo ""
        echo "✅ Published to PyPI!"
        echo ""
        echo "Install with:"
        echo "  pip install orbit-macos"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Release complete!"
echo ""
echo "📊 Verify at:"
if [ "$choice" = "1" ]; then
    echo "   https://test.pypi.org/project/orbit-macos/"
else
    echo "   https://pypi.org/project/orbit-macos/"
fi
