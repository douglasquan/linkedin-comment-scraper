# linkedin-comment-scraper

### Set Up Environment Variables

The process of setting up environment variables varies depending on the operating system you are using.

For Windows:

1. Open the Start Search, type in "Environment Variables," and select "Edit the system environment variables".
2. In the System Properties window, click the "Environment Variables" button.
3. In the Environment Variables window, you can add new variables by clicking the "New" button under the "System variables" or "User variables" section:
    - Variable name: LINKEDIN_EMAIL
    - Variable value: your-email@example.com
    - Repeat for LINKEDIN_PASSWORD.

For macOS and Linux:

1. Open your terminal.
2. Edit your shell profile file (e.g., ~/.bashrc, ~/.zshrc for bash and zsh respectively):

<code>export LINKEDIN_EMAIL="your-email@example.com"
export LINKEDIN_PASSWORD="your-password"
</code>

3. Save the file and run source ~/.bashrc or source ~/.zshrc to apply the changes.
