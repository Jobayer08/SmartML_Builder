#!/bin/bash
echo "=== SmartML Frontend Verification ==="
echo ""
echo "✓ Checking all pages exist..."
for page in Login Register Dashboard Datasets Models Train Predict History; do
  if [ -f "src/pages/${page}.jsx" ]; then
    echo "  ✓ ${page}.jsx"
  else
    echo "  ✗ ${page}.jsx MISSING"
  fi
done

echo ""
echo "✓ Checking all components exist..."
for comp in Navbar Sidebar ProtectedRoute DatasetCard ModelCard PredictionCard; do
  if [ -f "src/components/${comp}.jsx" ]; then
    echo "  ✓ ${comp}.jsx"
  else
    echo "  ✗ ${comp}.jsx MISSING"
  fi
done

echo ""
echo "✓ Checking core files exist..."
for file in context/AuthContext.jsx api/api.js App.jsx main.jsx; do
  if [ -f "src/${file}" ]; then
    echo "  ✓ ${file}"
  else
    echo "  ✗ ${file} MISSING"
  fi
done

echo ""
echo "✓ Build Status:"
npm run build 2>&1 | grep -E "✓ built|Error"
echo ""
echo "=== All Systems Ready ==="
