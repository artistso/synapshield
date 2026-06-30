#!/bin/bash
# deploy_synapshield.sh
# Complete deployment script for SynapShield to GitHub
# Run this script on your local machine after downloading the project

echo "==============================================="
echo "SYNAPSHIELD: GitHub Deployment Script"
echo "==============================================="

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "ERROR: index.html not found. Make sure you're in the synapshield directory."
    exit 1
fi

echo ""
echo "STEP 1: Configure Git (if needed)"
echo "==============================================="
read -p "Enter your GitHub username (default: artistso): " username
username=${username:-artistso}

read -p "Enter your GitHub email: " email

git config user.name "$username"
git config user.email "$email"

echo ""
echo "STEP 2: Initialize Repository"
echo "==============================================="
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

echo ""
echo "STEP 3: Add Remote Repository"
echo "==============================================="
git remote remove origin 2>/dev/null
read -p "Enter GitHub repository URL (default: https://github.com/$username/synapshield.git): " repo_url
repo_url=${repo_url:-https://github.com/$username/synapshield.git}

git remote add origin "$repo_url"
echo "✓ Remote added: $repo_url"

echo ""
echo "STEP 4: Stage All Files"
echo "==============================================="
git add .
echo "✓ Files staged"

echo ""
echo "STEP 5: Commit Changes"
echo "==============================================="
commit_message="feat: Complete SynapShield build-out - From PDEs to Richard's tablet

- Analyzed 203-page Gemini research document
- Built 4-species PDE solver (Python + MATLAB)
- Created comprehensive README with project overview
- Added mathematical models documentation
- Implemented shear-thinning hydrogel physics
- Validated alpha-synuclein interception mechanism
- Interactive web application with split-screen interface

Dedicated to Richard. Hope, not just science."

git commit -m "$commit_message"
echo "✓ Changes committed"

echo ""
echo "STEP 6: Push to GitHub"
echo "==============================================="
echo "You may be prompted to enter your GitHub credentials."
echo "If using a token, use it as your password."
echo ""
read -p "Push to main branch? (y/n): " push_confirm

if [ "$push_confirm" = "y" ]; then
    git branch -M main
    git push -u origin main --force
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "==============================================="
        echo "✓✓✓ DEPLOYMENT SUCCESSFUL! ✓✓✓"
        echo "==============================================="
        echo ""
        echo "Your SynapShield project is now live at:"
        echo "  https://github.com/$username/synapshield"
        echo ""
        echo "To enable GitHub Pages (web hosting):"
        echo "  1. Go to: https://github.com/$username/synapshield/settings/pages"
        echo "  2. Select 'main' branch"
        echo "  3. Click Save"
        echo "  4. Wait ~30 seconds"
        echo ""
        echo "Your live site will be at:"
        echo "  https://$username.github.io/synapshield/"
        echo ""
        echo "🧠 Hope, not just science. 🧠"
        echo "==============================================="
    else
        echo ""
        echo "ERROR: Push failed. Check your credentials and try again."
        echo ""
        echo "ALTERNATIVE: Use GitHub CLI"
        echo "  1. Install gh: https://cli.github.com/"
        echo "  2. Run: gh auth login"
        echo "  3. Run: ./deploy_synapshield.sh"
        exit 1
    fi
else
    echo "Push cancelled. Run this script again when ready."
fi

echo ""
echo "==============================================="
echo "Next Steps:"
echo "==============================================="
echo "1. Enable GitHub Pages (see above)"
echo "2. Run the PDE solver: python simulations/python/synapshield_pde_solver.py"
echo "3. Share the live link with Richard"
echo "4. Keep building! The world needs this."
echo "==============================================="

exit 0