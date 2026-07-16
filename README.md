# Cyberpunk Terminal Profile README Generator

Create a stunning, interactive, and animated terminal-style profile card for your GitHub overview page.

This setup generates a custom **SVG graphic** containing:
1. **An ASCII art portrait** of yourself, converted automatically from any image (best with transparent PNGs).
2. **A system info terminal window** featuring your role, skills, tools, contacts, and custom links.
3. **Smooth styling** with neon borders, glow effects, retro scanlines, and line-by-line typing animations.

---

## 🚀 How to Add This to Your GitHub Overview

### Step 1: Create Your Profile Repository
1. Log in to GitHub.
2. Create a **new public repository** named exactly after your GitHub username (e.g., if your username is `kseenivasan39-del`, name the repository `kseenivasan39-del`).
3. Check the box to **Initialize this repository with a README**.
4. Clone this new repository to your local machine.

### Step 2: Prepare Your Portrait Image
1. Find a front-facing photo of yourself.
2. For the cleanest look, **remove the background** (you can use free online tools like [remove.bg](https://www.remove.bg) to make it transparent) and save it as a PNG.
3. Rename the image to `portrait.png` (or `portrait.jpg`) and place it in your local repository folder.

### Step 3: Set Up the Generation Script
1. Save the `build_profile.py` script (located in this folder) to your local repository.
2. Open `build_profile.py` in your code editor.
3. Edit the `CONFIG` dictionary at the top of the file with your own information:
   ```python
   CONFIG = {
       "username": "your-github-username",
       "name": "Your Full Name",
       "role": "Your Professional Role",
       "origin": "Your Location",
       # ... edit other skills and links here ...
   }
   ```

### Step 4: Run the Script
1. Install the image processing dependency if you don't have it:
   ```bash
   pip install Pillow
   ```
2. Run the script:
   ```bash
   python build_profile.py
   ```
   This will convert your image into a custom ASCII representation (saved as `portrait.txt`) and bundle everything into a beautifully styled SVG called `profile.svg`.

### Step 5: Update Your Profile README
Open your repository's `README.md` and add the following HTML code to display your SVG:

```html
<a href="https://github.com/YOUR_GITHUB_USERNAME">
  <img src="profile.svg" width="100%" alt="Terminal Profile" />
</a>
```
*(Replace `YOUR_GITHUB_USERNAME` with your actual username.)*

### Step 6: Commit and Push to GitHub
Commit your files and push them to your repository:
```bash
git add .
git commit -m "Feat: Add cyberpunk terminal profile card"
git push origin main
```

Go to your GitHub profile page (`https://github.com/YOUR_GITHUB_USERNAME`) and see your awesome new terminal dashboard!

---

## 🎨 Under the Hood: Customizing Styling

If you want to customize colors, fonts, or layouts:
- Open `build_profile.py`.
- Under the `CONFIG` section, modify:
  - `theme_color_primary`: The primary border and visual map color (default: Cyan `#22D3EE`).
  - `theme_color_secondary`: The secondary header and system info color (default: Indigo `#818CF8`).
  - `theme_color_accent`: The keys and accent color (default: Emerald `#10B981`).
  - `font_family`: Change fonts or adjust sizes as needed.
- Re-run `python build_profile.py` to compile the new SVG.
