# GALIAS 🚀

**Terminal-based ImprovMX alias manager with hacker-chic style**

GALIAS is a sleek command-line tool for managing your ImprovMX email aliases. Create, delete, and list aliases with style - no browser needed!

```
 ██████╗  █████╗ ██╗     ██╗ █████╗ ███████╗
██╔════╝ ██╔══██╗██║     ██║██╔══██╗██╔════╝
██║  ███╗███████║██║     ██║███████║███████╗
██║   ██║██╔══██║██║     ██║██╔══██║╚════██║
╚██████╔╝██║  ██║███████╗██║██║  ██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝

ImprovMX Alias Manager @ yourdomain.com
```

## ✨ Features

- **🎨 Hacker-chic interface** with ASCII banners and styled output
- **⚡ Fast operations** - add, delete, list aliases in seconds
- **📊 Real-time progress** - see your alias count with visual progress bars
- **🔒 Secure authentication** using ImprovMX API keys
- **💻 Interactive prompts** - no need to remember command syntax
- **📋 JSON output** for scripting and automation
- **🎯 Smart error handling** with helpful error messages

## 🚀 Quick Start

### Super Simple Setup (Works Immediately!)

```bash
git clone https://github.com/gazzycodes/galias.git
cd galias
cp .env.example .env
```

**That's it!** Edit `.env` with your credentials and start using:

```bash
# Windows
.\galias.bat --version
.\galias.bat list
.\galias.bat add
.\galias.bat delete

# macOS/Linux
./galias --version
./galias list
./galias add
./galias delete
```

### Configure Environment

Edit `.env` with your ImprovMX credentials:
```env
IMPROVMX_API_KEY=sk_your_api_key_here
DOMAIN=yourdomain.com
```

**No installation, no PATH setup, no complications - just works!**

## 📖 Commands

### `list` - Show all aliases
```bash
galias list [OPTIONS]
```

**Options:**
- `--json` - Output raw JSON for scripting
- `--no-color` - Disable colored output
- `-q, --quiet` - Skip banner and just show aliases

**Example:**
```bash
galias list
[#####---------------] 5/25 aliases

┌─────────────────── Current Aliases ───────────────────┐
│ Alias    │ Forward To           │ Status    │
├──────────┼─────────────────────┼───────────┤
│ info     │ me@personal.com      │ ✓ Active  │
│ support  │ help@company.com     │ ✓ Active  │
│ hello    │ contact@domain.com   │ ✓ Active  │
└──────────┴─────────────────────┴───────────┘
```

### `add` - Create new alias
```bash
galias add [ALIAS] [FORWARD] [OPTIONS]
```

**Arguments:**
- `ALIAS` - Alias name (without domain)
- `FORWARD` - Email address to forward to

**Options:**
- `--json` - Output raw JSON for scripting
- `--no-color` - Disable colored output
- `-q, --quiet` - Skip banner and progress display

**Examples:**
```bash
# Interactive mode
galias add
❯ Enter new alias: sales
❯ Forward to: sales@company.com

# Direct mode
galias add sales sales@company.com
```

### `delete` - Remove alias
```bash
galias delete [ALIAS] [OPTIONS]
```

**Arguments:**
- `ALIAS` - Alias name to delete

**Options:**
- `-f, --force` - Skip confirmation prompt
- `--json` - Output raw JSON for scripting
- `--no-color` - Disable colored output
- `-q, --quiet` - Skip banner and progress display

**Examples:**
```bash
# Interactive mode with confirmation
galias delete
❯ Alias to delete: old-alias
❯ Delete alias 'old-alias'? [y/N]: y

# Direct mode
galias delete old-alias --force
```

### `status` - Show alias count and usage
```bash
galias status [OPTIONS]
```

**Options:**
- `--json` - Output raw JSON for scripting
- `--no-color` - Disable colored output

## 🔧 Configuration

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and paste your real ImprovMX API key:
   ```ini
   IMPROVMX_API_KEY=sk_b05673aeb5b0493891f61c4e5b5ba32f
   DOMAIN=yourdomain.com
   ```

3. Run any command (list, add, delete) and it will auto-load your credentials.

### Getting Your API Key

1. Log in to your [ImprovMX dashboard](https://improvmx.com/dashboard)
2. Go to **Account Settings** → **API**
3. Generate a new API key (starts with `sk_`)
4. Copy the key to your `.env` file

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `IMPROVMX_API_KEY` | Your ImprovMX API key | ✅ | - |
| `DOMAIN` | Your domain name | ✅ | - |
| `IMPROVMX_API_BASE_URL` | API base URL | ❌ | `https://api.improvmx.com` |
| `MAX_ALIASES` | Maximum aliases for your plan | ❌ | `25` |

## 🎨 Output Examples

### Progress Indicators
```bash
[#####---------------] 5/25 aliases          # Normal usage
[################----] 20/25 aliases ⚠️ 5 slots left    # Near limit
[####################] 25/25 aliases ⚠️ LIMIT REACHED   # At limit
```

### Success Messages
```bash
✓ Added alias: sales → sales@company.com
✓ Deleted alias: old-contact
```

### Error Messages
```bash
✗ Authentication failed
  Please check your API key in the .env file

✗ Alias already exists
  Choose a different alias name

✗ Network error
  Check your internet connection and try again
```

## 🔄 Scripting & Automation

Use `--json` flag for machine-readable output:

```bash
# Get alias count programmatically
galias status --json | jq '.current_aliases'

# List aliases in JSON format
galias list --json | jq '.aliases[].alias'

# Add alias silently
galias add bot bot@company.com --json --quiet
```

## 🐛 Troubleshooting

### Common Issues

**"galias: command not found" or "galias is not recognized"**
- The Python Scripts directory is not in your PATH
- **Solution 1:** Use the automated installer (`install.bat` on Windows or `python3 install.py` on macOS/Linux)
- **Solution 2:** Manually add Python Scripts directory to PATH
- **Solution 3:** Use `python -c "import improvctl; improvctl.main()" list` instead

**"✗ Missing IMPROVMX_API_KEY in .env"**
- Make sure your `.env` file exists and contains your API key
- Copy `.env.example` to `.env` and fill in your real API key

**"✗ Authentication failed"**
- Your API key is wrong or missing
- Check your API key in the ImprovMX dashboard
- Ensure your API key starts with `sk_` and has no extra spaces
- Verify you copied the complete key from the dashboard

**"✗ Invalid API key format"**
- ImprovMX API keys must start with `sk_`
- Check for typos or missing characters in your `.env` file

**"Network error"**
- Check your internet connection
- Verify the ImprovMX API is accessible

**"Alias limit reached"**
- You've hit your plan's alias limit (usually 25 for free plans)
- Delete some aliases or upgrade your plan

**"Alias already exists"**
- Choose a different alias name
- Check existing aliases with `python improvctl.py list`

**"No such alias"**
- Verify the alias name spelling
- List current aliases to see available options

### Debug Mode

For detailed error information, run with Python's verbose mode:
```bash
python -v -c "import galias; galias.main()"
```

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🔗 Links

- [ImprovMX](https://improvmx.com) - Email forwarding service
- [ImprovMX API Documentation](https://improvmx.com/api) - Official API docs

---

**Made with ❤️ for the terminal enthusiasts**
