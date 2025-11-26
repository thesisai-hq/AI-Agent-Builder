# Ollama Setup Guide for Finance Students

Complete guide to setting up free, local AI for investment analysis.

---

## What is Ollama?

**Ollama** is a free, open-source tool that lets you run AI models (like ChatGPT) on your own computer.

**Why use Ollama?**
- ✅ **Completely Free** - No API fees, unlimited use
- ✅ **Private** - Your data never leaves your computer
- ✅ **No Rate Limits** - Analyze as many stocks as you want
- ✅ **Works Offline** - No internet needed after setup
- ✅ **Educational** - Perfect for students learning

**Perfect for:**
- Students on a budget
- Learning investment analysis
- Testing and experimentation
- Privacy-sensitive analysis

---

## System Requirements

**Minimum:**
- 8GB RAM (for smaller models like llama3.2)
- 10GB free disk space (for model files)
- Modern CPU (Intel i5 or better, or Apple M1+)

**Recommended:**
- 16GB+ RAM (for better performance)
- 20GB+ free disk space (for multiple models)
- GPU optional (makes it faster but not required)

**Works on:**
- ✅ macOS (M1/M2 Macs work great!)
- ✅ Linux (Ubuntu, Fedora, etc.)
- ✅ Windows (via WSL2 - see below)

---

## Installation

### macOS (Easiest!)

```bash
# One command installs everything
curl https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

**Done!** Ollama is installed.

---

### Linux

#### Ubuntu / Debian

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Verify
ollama --version

# If permission issues
sudo chmod +x /usr/local/bin/ollama
```

#### Fedora / RHEL

```bash
# Install
curl https://ollama.ai/install.sh | sh

# Or manual install
sudo dnf install ollama

# Verify
ollama --version
```

---

### Windows (via WSL2)

**Step 1: Install WSL2**

```powershell
# In PowerShell (as Administrator)
wsl --install

# Restart computer when prompted
```

**Step 2: Open Ubuntu (WSL)**

```bash
# After restart, open "Ubuntu" from Start menu

# Install Ollama in WSL
curl https://ollama.ai/install.sh | sh

# Verify
ollama --version
```

**Note:** AI-Agent-Builder GUI works great in WSL2!

---

## Downloading Models

After installing Ollama, you need to download an AI model.

### Recommended Models for Finance Students

#### 1. llama3.2 (Recommended - Best Balance) ⭐

```bash
ollama pull llama3.2
```

**Size:** ~2GB  
**Speed:** Fast (2-3 seconds per analysis)  
**Quality:** Very good  
**Best for:** General stock analysis, learning

**Why we recommend this:**
- Latest Meta Llama model
- Good balance of speed and intelligence
- Perfect for finance education
- Works well on 8GB RAM

---

#### 2. mistral (Alternative - Faster)

```bash
ollama pull mistral
```

**Size:** ~4GB  
**Speed:** Very fast (1-2 seconds)  
**Quality:** Good  
**Best for:** Quick analysis, testing

---

#### 3. phi (Lightweight - For Older Computers)

```bash
ollama pull phi
```

**Size:** ~1.5GB  
**Speed:** Very fast  
**Quality:** Decent  
**Best for:** Low-memory systems, testing

---

### Checking Downloaded Models

```bash
# See what models you have
ollama list

# Should show something like:
# NAME            SIZE    MODIFIED
# llama3.2:latest 2.0GB   2 hours ago
```

---

## Starting Ollama

**You need to start Ollama service before using LLM agents!**

### Option 1: Start in Terminal (Recommended for Beginners)

```bash
# Open a terminal and run:
ollama serve

# You'll see:
# Ollama running on http://localhost:11434
```

**Keep this terminal window open!** Ollama needs to run while you use agents.

**When done:**
- Press `Ctrl+C` to stop
- Or just close the terminal

---

### Option 2: Background Service (Advanced)

#### macOS

```bash
# Start as background service
brew services start ollama

# Stop service
brew services stop ollama

# Check if running
brew services list | grep ollama
```

#### Linux (systemd)

```bash
# Start service
sudo systemctl start ollama

# Enable on boot (optional)
sudo systemctl enable ollama

# Stop service
sudo systemctl stop ollama

# Check status
systemctl status ollama
```

---

## Verifying Ollama Works

**Test 1: Check if service is running**

```bash
# In a new terminal (keep ollama serve running)
curl http://localhost:11434/api/tags

# Should show list of your models
```

**Test 2: Test a simple query**

```bash
ollama run llama3.2 "What is ROE in investing?"

# Should get an AI response about Return on Equity
```

**If both work:** ✅ Ollama is ready!

---

## Using Ollama with AI-Agent-Builder

### Step 1: Start Ollama

```bash
# In one terminal
ollama serve

# Keep this running
```

### Step 2: Launch GUI

```bash
# In another terminal
cd ~/AI-Agent-Builder
./gui/launch.sh
```

### Step 3: Create LLM Agent

1. Go to **➕ Create Agent**
2. Select **LLM-Powered** type
3. Configuration:
   - Provider: **ollama**
   - Model: **llama3.2**
   - Temperature: 0.5
   - Max Tokens: 1500
4. Click **Generate Code** → **Save Agent**

### Step 4: Test Agent

1. Go to **🧪 Test Agent**
2. Select your LLM agent
3. Choose Mock Data or YFinance
4. Click **Run Analysis**

**Should see:** AI-generated analysis!

---

## Troubleshooting

### ❌ "Can't connect to Ollama"

**Problem:** Ollama service not running

**Solution:**
```bash
# In a terminal
ollama serve

# Keep it running
```

**How to check:**
```bash
curl http://localhost:11434/api/tags
```

If you see `curl: (7) Failed to connect`, Ollama is not running.

---

### ❌ "Model 'llama3.2' not found"

**Problem:** Model not downloaded

**Solution:**
```bash
# Download the model
ollama pull llama3.2

# Verify it's there
ollama list
```

---

### ❌ "Ollama service port already in use"

**Problem:** Ollama already running (or something else using port 11434)

**Solutions:**

1. **Check if Ollama already running:**
```bash
# Try this first
curl http://localhost:11434/api/tags

# If you get a response, Ollama is already running!
# No need to run `ollama serve` again
```

2. **Kill existing Ollama:**
```bash
# macOS/Linux
pkill ollama

# Then start fresh
ollama serve
```

3. **Use different port:**
```bash
OLLAMA_HOST=127.0.0.1:11435 ollama serve

# Then update .env:
# OLLAMA_BASE_URL=http://localhost:11435
```

---

### ❌ "Out of memory" or very slow

**Problem:** Model too large for your RAM

**Solutions:**

1. **Use smaller model:**
```bash
# Try phi instead of llama3.2
ollama pull phi

# Update GUI to use phi model
```

2. **Close other programs:**
- Close browser tabs
- Close heavy applications
- Free up RAM

3. **Increase system swap:**
```bash
# Linux - increase swap space
sudo swapon --show
```

---

### ❌ "Model download fails"

**Problem:** Network issue or not enough disk space

**Solutions:**

1. **Check disk space:**
```bash
df -h

# Need at least 5GB free
```

2. **Check internet:**
```bash
ping ollama.ai
```

3. **Try different mirror:**
```bash
# Try again later
ollama pull llama3.2
```

---

## Performance Tips

### Speed Up Analysis

**1. Use smaller models for testing:**
```bash
# Phi is faster than llama3.2
ollama pull phi
```

**2. Lower max_tokens:**
- In GUI: Set Max Tokens to 800 instead of 1500
- Faster responses, still good quality

**3. Close other programs:**
- Free up RAM and CPU
- Ollama gets more resources

---

### Save Disk Space

**Remove models you don't use:**
```bash
# List models
ollama list

# Remove a model
ollama rm mistral

# Keep only llama3.2 for finance
```

---

## Comparing Ollama to Cloud AI

### Ollama (Free, Local)

**Pros:**
- ✅ Free forever
- ✅ Unlimited analyses
- ✅ Private (data stays local)
- ✅ Works offline
- ✅ No rate limits

**Cons:**
- ❌ Slower (2-5 seconds vs <1 second)
- ❌ Requires good computer (8GB+ RAM)
- ❌ Must keep service running
- ❌ Setup required

**Best for:** Students, learning, testing, privacy

---

### OpenAI / Anthropic (Paid, Cloud)

**Pros:**
- ✅ Very fast (<1 second)
- ✅ More capable models
- ✅ No local setup
- ✅ Works on any computer

**Cons:**
- ❌ Costs $0.01-0.03 per analysis
- ❌ Rate limits (requests per minute)
- ❌ Requires internet
- ❌ Data sent to third party

**Best for:** Production, speed-critical, when budget allows

**Cost Example:**
- 10 stocks/day: ~$3/month
- 50 stocks/day: ~$15/month
- 200 stocks/day: ~$60/month

---

## Recommended Setup for Students

### For Learning (Recommended)

```bash
# 1. Install Ollama
curl https://ollama.ai/install.sh | sh

# 2. Download llama3.2 (best for learning)
ollama pull llama3.2

# 3. Start Ollama
ollama serve

# 4. Use AI-Agent-Builder GUI
./gui/launch.sh

# Cost: $0
# Speed: Good enough for learning
# Privacy: Complete
```

---

### For Advanced Students (Multiple Models)

```bash
# Download multiple models for different uses
ollama pull llama3.2  # General analysis
ollama pull phi       # Quick testing
ollama pull mistral   # Alternative

# Use different models for different agents
# Experiment to see which you prefer
```

---

## Common Questions

### Q: Do I need to download models every time?

**A:** No! Download once, use forever.

Models are saved to:
- macOS: `~/.ollama/models/`
- Linux: `~/.ollama/models/`
- Windows: `%USERPROFILE%\.ollama\models\`

---

### Q: Can I use Ollama and OpenAI together?

**A:** Yes! Create some agents with Ollama (free) and some with OpenAI (better quality).

---

### Q: How much disk space do models use?

**A:**
- phi: ~1.5GB
- llama3.2: ~2GB
- mistral: ~4GB
- llama3.1: ~5GB

Keep what you need, delete what you don't use.

---

### Q: Is Ollama legal to use?

**A:** Yes! Ollama and the models are open-source and free to use.

---

### Q: Can I use Ollama for real trading?

**A:** Ollama is fine for analysis, but remember:
- AI-Agent-Builder is educational only
- Not financial advice
- Consult professionals for real trading
- See [DISCLAIMER.md](../DISCLAIMER.md)

---

## Next Steps

✅ **Setup Complete?** Try these:

1. **Create your first LLM agent**
   - Go to GUI → Create Agent → LLM-Powered
   - Use Ollama + llama3.2
   - Test with mock data

2. **Compare to rules**
   - Create same strategy as rule-based agent
   - Compare results
   - See how LLM reasoning differs

3. **Experiment with temperature**
   - Try temperature 0.2 (conservative)
   - Try temperature 0.8 (creative)
   - See how it changes analysis

4. **Try hybrid agent**
   - Use rules to filter (fast)
   - Use Ollama for deep analysis (smart)
   - Get efficiency at scale

5. **Read the comprehensive guide**
   - In GUI → How to Use Agents → LLM Agents tab
   - Detailed explanations
   - Real examples

---

## Getting Help

**If Ollama won't work:**

1. Check [Troubleshooting](#troubleshooting) section above
2. Read [Ollama Documentation](https://ollama.ai/docs)
3. Check [AI-Agent-Builder Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
4. Ask in class or study group

**For AI-Agent-Builder issues:**
- See [Data Flow](DATA_FLOW.md) - Understand how LLM agents work ⭐
- See [LLM Customization](LLM_CUSTOMIZATION.md) - Advanced LLM configuration
- See [GUI Quick Start](../GUI_QUICK_START.md) - GUI guide
- See [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- Run `python3 gui/test_setup.py`

---

## Summary

**Quick Setup:**
```bash
# 1. Install
curl https://ollama.ai/install.sh | sh

# 2. Download model
ollama pull llama3.2

# 3. Start service
ollama serve  # Keep running

# 4. Use in GUI
./gui/launch.sh
```

**Remember:**
- ✅ Free and unlimited
- ✅ Privacy-friendly
- ✅ Great for learning
- ✅ Keep `ollama serve` running
- ⚠️ Educational use only

**You're ready to use AI for investment analysis!** 🚀

---

**Updated:** 2025-01-14  
**For:** AI-Agent-Builder v1.0.0  
**License:** MIT - See [LICENSE](../LICENSE)
