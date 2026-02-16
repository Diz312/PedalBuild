# PedalBuild Documentation Index

**Last Updated**: 2026-02-16
**Status**: Phase 2 Complete (Backend API + Database Foundation)

---

## 🎯 Where to Start

| I want to... | Read this |
|-------------|-----------|
| **Resume work after a break** | [PROJECT_STATUS.md](PROJECT_STATUS.md) ⭐ |
| **Get started quickly** | [QUICKSTART.md](QUICKSTART.md) |
| **Understand the project** | [README.md](README.md) |
| **Build new features** | [CLAUDE.md](CLAUDE.md) |
| **Use the API** | [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) |

---

## 📚 All Documentation

### Getting Started (Start Here!)

#### **[PROJECT_STATUS.md](PROJECT_STATUS.md)** ⭐
**Purpose**: Current status, what's complete, what's next, how to resume
**When to read**: Every time you return to the project
**Contains**:
- Quick resume guide (3 commands to start working)
- What's complete (Phases 1-2)
- Current capabilities
- Test status
- Next steps (Phase 3 - Frontend)
- File locations reference
- Common commands

#### **[QUICKSTART.md](QUICKSTART.md)**
**Purpose**: Quick command reference card
**When to read**: Need a command fast
**Contains**:
- Start server (3 commands)
- Common commands cheat sheet
- API endpoint quick reference
- Import inventory examples
- Testing examples

#### **[README.md](README.md)**
**Purpose**: Project overview and installation
**When to read**: First time seeing the project, showing to others
**Contains**:
- Project overview
- 10-stage workflow description
- Features list
- Installation instructions
- Technology stack
- Project structure
- Current status

---

### Development Guides

#### **[CLAUDE.md](CLAUDE.md)**
**Purpose**: Comprehensive project guide for Claude Code
**When to read**: Building features, understanding architecture
**Contains**:
- Critical user requirements (NON-NEGOTIABLE!)
- Python tooling setup
- Architecture principles
- Project structure
- Database schema patterns
- Type system details
- Workflow stages (10 stages)
- REST API endpoints (16 endpoints)
- Custom tools usage
- Important patterns
- User preferences
- Phase 2 completion status

#### **[PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md)**
**Purpose**: Python setup, tooling, and workflow
**When to read**: Setting up dev environment, questions about tooling
**Contains**:
- Why we chose these tools (uv, ruff, mypy, black)
- Complete setup guide
- Tooling configuration
- Type synchronization workflow
- Pre-commit hooks
- Common commands
- Troubleshooting

#### **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)**
**Purpose**: Complete REST API reference
**When to read**: Working with API endpoints, integrating frontend
**Contains**:
- All 16 endpoints documented
- Request/response examples
- Query parameters
- Error handling
- CSV import format specification
- curl examples
- HTTPie examples
- Testing guide

#### **[CLAUDE_CODE_TOOLS.md](CLAUDE_CODE_TOOLS.md)**
**Purpose**: Claude Code development tools (skills + sub-agents)
**When to read**: Using Claude Code to build, troubleshooting tools
**Contains**:
- Universal skills documentation
- Universal sub-agents documentation
- Project-specific tools (not yet built)
- Usage examples

---

### Reference Documentation

#### **[docs/ELECTRONICS_REFERENCE.md](docs/ELECTRONICS_REFERENCE.md)**
**Purpose**: Guitar pedal electronics knowledge base
**When to read**: Understanding pedal circuits, component substitutions
**Contains**:
- Component types and values
- Circuit types (fuzz, distortion, overdrive, etc.)
- Breadboard platform specification
- Common substitutions
- Testing procedures

---

## 📁 File Organization

### Documentation Files (Root Level)
```
PROJECT_STATUS.md          ⭐ Start here to resume
QUICKSTART.md              Quick commands
README.md                  Project overview
CLAUDE.md                  Complete development guide
PYTHON_DEVELOPMENT.md      Python setup & tooling
CLAUDE_CODE_TOOLS.md       Development tools
DOCUMENTATION_INDEX.md     This file
```

### Documentation Files (docs/ Directory)
```
docs/
├── API_DOCUMENTATION.md        Complete API reference
└── ELECTRONICS_REFERENCE.md    Electronics knowledge base
```

### Archived/Generated Documentation
```
BACKEND_COMPLETE.md        Summary of Phase 2 work (archived)
.pytest_cache/README.md    Pytest cache info (auto-generated)
```

---

## 🎯 Documentation by Use Case

### "I'm New to This Project"
1. Read [README.md](README.md) - Understand what PedalBuild is
2. Read [PROJECT_STATUS.md](PROJECT_STATUS.md) - See current status
3. Read [QUICKSTART.md](QUICKSTART.md) - Try running it
4. Read [CLAUDE.md](CLAUDE.md) - Deep dive when building

### "I'm Resuming After a Break"
1. Read [PROJECT_STATUS.md](PROJECT_STATUS.md) - What's done, what's next
2. Run the 3 commands in Quick Resume section
3. Check [QUICKSTART.md](QUICKSTART.md) for commands
4. Refer to [CLAUDE.md](CLAUDE.md) when building features

### "I'm Building the Frontend"
1. Read [PROJECT_STATUS.md](PROJECT_STATUS.md) - Phase 3 tasks
2. Read [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Understand API
3. Read [CLAUDE.md](CLAUDE.md) - User requirements, architecture
4. Use [QUICKSTART.md](QUICKSTART.md) for testing API

### "I'm Working on the Backend"
1. Read [PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md) - Tooling setup
2. Read [CLAUDE.md](CLAUDE.md) - Architecture patterns
3. Read [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Existing API
4. Use [QUICKSTART.md](QUICKSTART.md) for common commands

### "I'm Building AI Agents"
1. Read [CLAUDE.md](CLAUDE.md) - Critical requirements (multi-pass analysis!)
2. Read [docs/ELECTRONICS_REFERENCE.md](docs/ELECTRONICS_REFERENCE.md) - Domain knowledge
3. Read [CLAUDE_CODE_TOOLS.md](CLAUDE_CODE_TOOLS.md) - Tools reference

### "I'm Testing/Debugging"
1. Read [QUICKSTART.md](QUICKSTART.md) - Test commands
2. Read [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - API examples
3. Read [PYTHON_DEVELOPMENT.md](PYTHON_DEVELOPMENT.md) - Debugging tools

---

## 📝 Documentation Standards

### Keep Updated
- **PROJECT_STATUS.md** - Update after completing phases/major work
- **README.md** - Update status section when phases complete
- **CLAUDE.md** - Update "Last Updated" and "Next Steps" sections
- **docs/API_DOCUMENTATION.md** - Update when adding/changing endpoints

### Archive When Obsolete
- Implementation plans after completion → Keep for reference
- Phase summaries after consolidation → Archive or delete

### Never Edit
- Auto-generated files (types.generated.ts, types.ts)
- Pytest cache files
- Git-ignored files

---

## 🎬 What Each Phase Needs

### Phase 1 (Complete) ✅
- ✅ PYTHON_DEVELOPMENT.md created
- ✅ CLAUDE.md updated
- ✅ README.md status updated

### Phase 2 (Complete) ✅
- ✅ PROJECT_STATUS.md created
- ✅ QUICKSTART.md created
- ✅ docs/API_DOCUMENTATION.md created
- ✅ DOCUMENTATION_INDEX.md created (this file)
- ✅ README.md updated
- ✅ CLAUDE.md updated

### Phase 3 (Frontend - Next)
- [ ] Update PROJECT_STATUS.md after completion
- [ ] Create docs/FRONTEND_GUIDE.md
- [ ] Update README.md with frontend setup
- [ ] Update QUICKSTART.md with frontend commands

### Phase 4 (AI Agents - Future)
- [ ] Create docs/AGENT_DEVELOPMENT.md
- [ ] Document agent architecture
- [ ] Document Google ADK integration
- [ ] Update CLAUDE.md with agent patterns

---

## 💡 Documentation Tips

### Writing New Docs
- **Be concise** - Developers scan, don't read
- **Use examples** - Show, don't just tell
- **Link liberally** - Connect related docs
- **Update index** - Add to this file when creating new docs

### Maintaining Docs
- **Review on phase completion** - Ensure accuracy
- **Remove outdated info** - Don't accumulate cruft
- **Consolidate duplicates** - One source of truth
- **Check links** - Ensure they work

### For Future You
- **Document decisions** - Why, not just what
- **Note gotchas** - Things that tripped you up
- **Show workflows** - Step-by-step processes
- **Keep status current** - PROJECT_STATUS.md is key

---

## 🔗 External Resources

- **Google ADK Docs**: https://google.github.io/adk-docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js 15 Docs**: https://nextjs.org/docs
- **Shadcn UI**: https://ui.shadcn.com/
- **Pydantic V2**: https://docs.pydantic.dev/latest/
- **PedalPCB**: https://www.pedalpcb.com/

---

## 📊 Documentation Statistics

- **Total Markdown Files**: 9 core documentation files
- **Total Pages**: ~100 pages of documentation
- **Most Important**: PROJECT_STATUS.md (resume guide)
- **Most Comprehensive**: CLAUDE.md (project guide)
- **Most Referenced**: QUICKSTART.md (commands)

---

**Maintained By**: Project contributors
**Update Frequency**: After each phase completion
**Format**: Markdown with GitHub Flavored Markdown extensions

---

**Need help?** Start with [PROJECT_STATUS.md](PROJECT_STATUS.md) - it's your resume point! 🚀
