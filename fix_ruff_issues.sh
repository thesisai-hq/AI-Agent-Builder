#!/bin/bash

# Fix Remaining Ruff Issues
# This script fixes the 18 remaining linting issues

echo "🔧 Fixing Remaining Ruff Issues..."
echo "===================================="
echo ""

# Fix 1: Update pyproject.toml (deprecated config format)
echo "1. Updating pyproject.toml lint configuration..."
if [ -f "pyproject.toml" ]; then
    # This will be done manually or with sed
    echo "   ⚠️  Manual fix needed: Move lint settings to [tool.ruff.lint] section"
    echo "   See: pyproject.toml"
else
    echo "   ⚠️  pyproject.toml not found"
fi

# Fix 2: Import checks in examples (intentional for checking dependencies)
echo ""
echo "2. Fixing import checks in examples..."
echo "   These are intentional (checking if packages installed)"
echo "   Adding # noqa: F401 comments to suppress warnings"

# Fix examples/02_llm_agent.py
if [ -f "examples/02_llm_agent.py" ]; then
    sed -i 's/import ollama$/import ollama  # noqa: F401/' examples/02_llm_agent.py 2>/dev/null || \
    sed -i '' 's/import ollama$/import ollama  # noqa: F401/' examples/02_llm_agent.py
    echo "   ✅ Fixed 02_llm_agent.py"
fi

# Fix examples/04_rag_agent.py  
if [ -f "examples/04_rag_agent.py" ]; then
    sed -i 's/import ollama$/import ollama  # noqa: F401/' examples/04_rag_agent.py 2>/dev/null || \
    sed -i '' 's/import ollama$/import ollama  # noqa: F401/' examples/04_rag_agent.py
    
    sed -i 's/import sentence_transformers$/import sentence_transformers  # noqa: F401/' examples/04_rag_agent.py 2>/dev/null || \
    sed -i '' 's/import sentence_transformers$/import sentence_transformers  # noqa: F401/' examples/04_rag_agent.py
    echo "   ✅ Fixed 04_rag_agent.py"
fi

# Fix 3: Bare except statements (add Exception type)
echo ""
echo "3. Fixing bare except statements..."

# Fix examples/02_llm_agent.py
if [ -f "examples/02_llm_agent.py" ]; then
    sed -i 's/        except:$/        except Exception:/' examples/02_llm_agent.py 2>/dev/null || \
    sed -i '' 's/        except:$/        except Exception:/' examples/02_llm_agent.py
    echo "   ✅ Fixed 02_llm_agent.py bare except"
fi

# Fix setup_test_db.py
if [ -f "setup_test_db.py" ]; then
    sed -i 's/    except:$/    except Exception:/' setup_test_db.py 2>/dev/null || \
    sed -i '' 's/    except:$/    except Exception:/' setup_test_db.py
    echo "   ✅ Fixed setup_test_db.py bare except"
fi

# Fix 4: Missing Backtester import in gui/app.py
echo ""
echo "4. Fixing missing Backtester import..."
echo "   ⚠️  Manual fix needed: Add Backtester import or comment out backtest page"
echo "   File: gui/app.py line ~1512"

# Fix 5: Unused imports in quickstart.py (intentional test file)
echo ""
echo "5. Fixing quickstart.py (test imports)..."
if [ -f "quickstart.py" ]; then
    # Add noqa comment to the import block
    echo "   ⚠️  Manual fix: These are intentional test imports"
    echo "   Consider adding # noqa: F401 or removing file"
fi

# Fix 6: test_wizard_python.py (will be deleted anyway)
echo ""
echo "6. test_wizard_python.py will be deleted in cleanup"
echo "   No action needed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Automatic fixes applied!"
echo ""
echo "⚠️  Manual fixes needed (2 files):"
echo ""
echo "1. pyproject.toml - Update lint config:"
echo "   Change [tool.ruff] section to [tool.ruff.lint]"
echo ""
echo "2. gui/app.py - Fix Backtester import:"
echo "   Either:"
echo "   - Add: from gui.backtester import Backtester"
echo "   - Or comment out show_backtest_page() if not needed"
echo ""
echo "3. quickstart.py - Either:"
echo "   - Add # noqa: F401 to unused imports"
echo "   - Or delete file if not needed"
echo ""
echo "After manual fixes, run:"
echo "  ruff check ."
echo ""
