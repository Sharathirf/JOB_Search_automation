# Git Commands Cheat Sheet 🚀

## 📝 The 6 Commands We Used

### 1. `git init`
**What**: Initialize Git in your folder  
**When**: First time only  
**Why**: Turn your folder into a Git repository

```bash
git init
```
**Result**: Creates `.git` folder (hidden)

---

### 2. `git remote add origin <URL>`
**What**: Connect to GitHub  
**When**: First time only  
**Why**: Tell Git where to push code

```bash
git remote add origin https://github.com/Sharathirf/JOB_Search_automation.git
```
**Result**: Linked to GitHub ✅

---

### 3. `git config user.email/name`
**What**: Set your identity  
**When**: First time only  
**Why**: Git needs to know who made changes

```bash
git config user.email "your@email.com"
git config user.name "Your Name"
```
**Result**: Your name on every commit

---

### 4. `git add .`
**What**: Stage files for commit  
**When**: Every time you have changes  
**Why**: Select which files to include

```bash
git add .              # Add all files
git add file.py        # Add one file
git add *.py           # Add all .py files
```
**Result**: Files ready to commit

---

### 5. `git commit -m "message"`
**What**: Save snapshot with message  
**When**: After adding files  
**Why**: Create a checkpoint of your code

```bash
git commit -m "Add duplicate detection"
```
**Result**: Code saved in history ✅

---

### 6. `git push -u origin main`
**What**: Upload to GitHub  
**When**: After committing  
**Why**: Share code online

```bash
git push -u origin main  # First time
git push                  # Later (simpler!)
```
**Result**: Code on GitHub ✅

---

## 🔄 Daily Workflow

```bash
# 1. Make changes to code
# Edit scrape_jobs.py

# 2. Check what changed
git status

# 3. Add changes
git add .

# 4. Commit with message
git commit -m "Fix bug in duplicate detection"

# 5. Push to GitHub
git push
```

**That's it!** ✅

---

## 📊 Our Commits

### Commit 1: Initial Upload (46e600c)
- Added 9 files
- 1,667 lines of code
- Initial version with all features

### Commit 2: Clean Up (0307b6e)
- Removed 4 redundant files
- Simplified README
- Final clean version

---

## 🎯 Key Concepts

| Concept | Analogy | Git Command |
|---------|---------|-------------|
| Repository | Bank Account | `git init` |
| Staging | Shopping Cart | `git add` |
| Commit | Photo | `git commit` |
| Push | Upload to Cloud | `git push` |
| Remote | Dropbox Link | `git remote add` |

---

## ⚠️ Important Rules

1. **Always commit before push** ✅
2. **Write clear commit messages** ✅
3. **Never commit credentials.json** ✅
4. **Check status before push** ✅

---

**Repository**: https://github.com/Sharathirf/JOB_Search_automation.git

