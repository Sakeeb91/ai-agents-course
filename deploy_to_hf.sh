#!/bin/bash

# Hugging Face Spaces Deployment Script
# Usage: ./deploy_to_hf.sh YOUR_HF_USERNAME

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================="
echo "  🚀 Hugging Face Spaces Deployment"
echo "========================================="
echo -e "${NC}"

# Check if username is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Please provide your Hugging Face username${NC}"
    echo -e "${YELLOW}Usage: ./deploy_to_hf.sh YOUR_HF_USERNAME${NC}"
    exit 1
fi

HF_USERNAME="$1"
SPACE_NAME="ai-agent-chat"
FULL_REPO="${HF_USERNAME}/${SPACE_NAME}"

echo -e "${BLUE}👤 Username: ${HF_USERNAME}${NC}"
echo -e "${BLUE}📦 Space: ${SPACE_NAME}${NC}"
echo ""

# Check if logged in
echo -e "${YELLOW}🔐 Checking Hugging Face login status...${NC}"
if ! huggingface-cli whoami &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Hugging Face${NC}"
    echo -e "${YELLOW}Please login first:${NC}"
    echo -e "  huggingface-cli login"
    exit 1
fi

CURRENT_USER=$(huggingface-cli whoami | head -n 1)
echo -e "${GREEN}✅ Logged in as: ${CURRENT_USER}${NC}"
echo ""

# Check if files exist
echo -e "${YELLOW}📂 Checking required files...${NC}"
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ app.py not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ app.py found${NC}"

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ requirements.txt found${NC}"
echo ""

# Ask to create Space if it doesn't exist
echo -e "${YELLOW}🌐 Checking if Space exists...${NC}"
if ! huggingface-cli repo info "spaces/${FULL_REPO}" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Space '${FULL_REPO}' not found${NC}"
    echo -e "${YELLOW}Would you like to create it? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}📝 Creating Space...${NC}"
        huggingface-cli repo create "${SPACE_NAME}" --type space --space_sdk gradio
        echo -e "${GREEN}✅ Space created successfully!${NC}"
    else
        echo -e "${RED}❌ Please create the Space manually at:${NC}"
        echo -e "   https://huggingface.co/new-space"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Space exists${NC}"
fi
echo ""

# Upload files
echo -e "${YELLOW}📤 Uploading files to Hugging Face...${NC}"
echo ""

echo -e "${BLUE}  → Uploading app.py...${NC}"
huggingface-cli upload "spaces/${FULL_REPO}" app.py app.py
echo -e "${GREEN}  ✅ app.py uploaded${NC}"

echo -e "${BLUE}  → Uploading requirements.txt...${NC}"
huggingface-cli upload "spaces/${FULL_REPO}" requirements.txt requirements.txt
echo -e "${GREEN}  ✅ requirements.txt uploaded${NC}"

echo ""
echo -e "${GREEN}"
echo "========================================="
echo "  ✅ Deployment Complete!"
echo "========================================="
echo -e "${NC}"

echo -e "${BLUE}🌐 Your Space is available at:${NC}"
echo -e "${GREEN}   https://huggingface.co/spaces/${FULL_REPO}${NC}"
echo ""

echo -e "${YELLOW}⚠️  IMPORTANT: Don't forget to add your API key!${NC}"
echo ""
echo -e "${BLUE}Steps to add API key:${NC}"
echo "  1. Visit: https://huggingface.co/spaces/${FULL_REPO}/settings"
echo "  2. Scroll to 'Repository secrets'"
echo "  3. Click 'New secret'"
echo "  4. Name: GOOGLE_API_KEY"
echo "  5. Value: AIzaSyBR3sPTYuwKGkBBkAKvV13vBrqxBAfWL6Q"
echo "  6. Click 'Save'"
echo ""

echo -e "${BLUE}📊 Your Space will build automatically (2-5 minutes)${NC}"
echo -e "${BLUE}🎉 Once ready, it will be available at:${NC}"
echo -e "${GREEN}   https://${HF_USERNAME}-${SPACE_NAME}.hf.space${NC}"
echo ""

echo -e "${YELLOW}Would you like to open the Space in your browser? (y/n)${NC}"
read -r open_browser
if [[ "$open_browser" =~ ^[Yy]$ ]]; then
    open "https://huggingface.co/spaces/${FULL_REPO}"
fi

echo ""
echo -e "${GREEN}✨ Happy chatting! ✨${NC}"
