# Google Cloud Setup for Gmail and Drive MCP Integration

## Prerequisites
- Google account with Gmail access
- Reports being sent to your Gmail inbox from OnVolunteers

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your Project ID

## Step 2: Enable Required APIs

Enable these APIs in your Google Cloud Console:
- Gmail API
- Google Drive API
- Google Sheets API (optional, for spreadsheet reports)
- Google Docs API (optional, for document reports)

Navigate to: `APIs & Services > Library` and search for each API to enable them.

## Step 3: Create OAuth 2.0 Credentials

1. Go to `APIs & Services > Credentials`
2. Click `+ CREATE CREDENTIALS > OAuth 2.0 Client ID`
3. If prompted, configure the OAuth consent screen first:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to Test users
4. For Application type, select "Desktop application"
5. Name it "OnVolunteers Report Automation"
6. Click "Create"
7. Download the JSON file (it will be named something like `client_secret_xxx.json`)

## Step 4: Configure MCP Servers

1. Rename the downloaded JSON file to `credentials.json`
2. Move it to: `/Users/michaelsew/work/onvolunteers-notebook/.config/gdrive/credentials.json`
3. Extract the CLIENT_ID and CLIENT_SECRET from the JSON file
4. Update your `.mcp/config.json` file:

Replace these lines in `.mcp/config.json`:
```json
"CLIENT_ID": "YOUR_GOOGLE_CLIENT_ID",
"CLIENT_SECRET": "YOUR_GOOGLE_CLIENT_SECRET",
```

With your actual values from the credentials.json file:
```json
"CLIENT_ID": "123456789-xxxxx.apps.googleusercontent.com",
"CLIENT_SECRET": "GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx",
```

## Step 5: Test the Setup

1. Restart Claude Code to reload the MCP configuration
2. The first time you use Gmail or Google Drive tools, you'll be prompted to authenticate via browser
3. Grant the necessary permissions for Gmail and Drive access

## Authentication Files Location

After first authentication, these files will be created:
- Gmail auth: `~/.cache/gmail-mcp/` (or similar)
- Google Drive auth: `/Users/michaelsew/work/onvolunteers-notebook/.config/gdrive/token.json`

## Troubleshooting

### Common Issues:
1. **"OAuth consent screen not configured"** - Complete Step 3 above
2. **"API not enabled"** - Enable all required APIs in Step 2
3. **"Invalid client"** - Double-check CLIENT_ID and CLIENT_SECRET in config
4. **"Permissions error"** - Make sure your email is added as a test user

### Testing Commands:
After setup, you can test with Claude Code:
- "Search my Gmail for emails from OnVolunteers"
- "List files in my Google Drive"
- "Download attachments from recent emails"

## Security Notes
- Keep your `credentials.json` and `token.json` files secure
- Add them to `.gitignore` to prevent committing to version control
- The OAuth setup uses "Desktop application" type for security