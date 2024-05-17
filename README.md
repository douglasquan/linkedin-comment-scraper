# LinkedIn Post Comment Scraper

## Overview

This tool is designed to scrape comments from LinkedIn posts, extracting detailed information about each commenter such as their name, current position, LinkedIn URL, and the comment text. The data is saved into a CSV file for further analysis.

## Prerequisites

- Python 3.6 or higher
- pip for installing Python packages
- Google Chrome 

    
## Set Up Environment Variables for Login Credentials 
To ensure full access to LinkedIn posts while maintaining security, it's recommended to use environment variables for storing your login credentials. This practice keeps sensitive information out of your source code and helps protect your main LinkedIn account from potential security risks associated with automated access.

For this setup, consider using a burner account to prevent any impact on your primary LinkedIn profile. A burner account is essentially a secondary account used specifically for automation to avoid potential flagging or restrictions that might be imposed on your main account due to automated activities.

Here are the credentials for a burner account we've set up for this purpose:

    Email: bobcousy671@gmail.com
    Password: kxQqaspT4$6v#1MTTY7R

Below are detailed instructions for setting up these credentials as environment variables on Windows, macOS, and Linux systems:

### For Windows Users:

1. Open System Properties:
    - Open the Start Search by pressing Win + S, type “Environment Variables” into the search box, and select “Edit the system environment variables”. This opens the System Properties window directly to the Advanced tab.

2. Access Environment Variables:
    - Click the “Environment Variables…” button near the bottom of the System Properties dialog.

3. Add New Environment Variables:
    - In the Environment Variables window, you’ll see two lists: User variables (just for your user account) and System variables (for the entire system).
    - Decide whether you want to set the variables for just your user account or for the entire system:
        - For User variables: Click “New…” under the User variables pane.
        - For System variables: Click “New…” under the System variables pane.

4. Set the Variables:
    - In the New User Variable dialog, enter LINKEDIN_EMAIL as the Variable name and enter your LinkedIn email as the Variable value. Click OK.
    - Repeat the process for LINKEDIN_PASSWORD: Enter LINKEDIN_PASSWORD as the Variable name and your LinkedIn password as the Variable value. Click OK.

5. Close the Dialogs:
    - After adding your variables, click OK in all dialogs to close them and apply the changes.

### For macOS and Linux Users:

1. Open Your Shell Configuration File:
    - Depending on which shell you use, open your shell configuration file (~/.bashrc for Bash, ~/.zshrc for Zsh, etc.) in a text editor. For most Linux distributions and macOS, Bash is the default shell:
    
        ```
        nano ~/.bashrc  # or substitute with your preferred editor
        ```
2. Add the Environment Variables:

    - Add the following lines to the end of the file to set up the LinkedIn credentials:

        ```
        export LINKEDIN_EMAIL="your-email@example.com"
        export LINKEDIN_PASSWORD="your-password"
        ```
    - Save the file and exit the editor.

3. Apply the Changes:

    - To make the changes effective, run source ~/.bashrc or source ~/.zshrc to apply the changes.
    
        ```
        source ~/.bashrc  # Or corresponding file like ~/.zshrc
        ```

## Installation

1. Clone the repository or download the source code.
2. Navigate to the directory containing the script.
3. Install required Python packages:

    ```      
    pip install -r requirements.txt
    ```

## Usage

1. Open your command line interface.
2. Execute the script with optional parameters:
   - <code>-r</code>: Load all replies to comments (optional but recommended).
   - <code>-o</code>: Specify the output CSV file name (optional, default is data-{current-time}.csv).

    ```
    python linkedin-scraper.py -r -o output_filename
    ```


3. Enter the LinkedIn post URL when prompted.

## Configuration

Edit the config.json file to match the HTML structure of the LinkedIn post if necessary. The default configuration should work for standard LinkedIn post layouts.

 ## Example

```
python linkedin-scraper.py -r -o my_scraped_data
```

This command will scrape all comments and replies from the specified LinkedIn post and save them in "my_scraped_data.csv".
## Notes

- Ensure that your version of ChromeDriver matches the version of Chrome installed on your machine.
- The scraping tool is intended for educational and professional purposes where allowed. Respect LinkedIn's terms of service during use.


