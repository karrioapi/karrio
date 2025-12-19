# Karrio Carrier Integration Agent PRD

## Overview

This document describes the architecture and implementation plan for an **autonomous carrier integration agent** that can build, test, and iterate on Karrio carrier integrations with minimal human intervention.

## Problem Statement

Building carrier integrations for Karrio is a repetitive, well-defined process that follows strict patterns:

1. **Scaffolding** - Using CLI to bootstrap extension structure
2. **Schema Population** - Adding carrier API request/response samples
3. **Code Generation** - Running schema-to-Python generators
4. **Implementation** - Writing provider logic, units, proxy, and settings
5. **Testing** - Creating and running unittest suites
6. **Validation** - Ensuring all success criteria are met

Currently, this process requires significant developer time and expertise. While the existing Karrio Studio UI provides manual controls and AI prompts, there's no automated feedback loop that can:

- Execute the full integration lifecycle autonomously
- Run tests and analyze failures
- Iterate on implementation until tests pass
- Self-validate against success criteria

## Proposed Solution

### Carrier Integration Agent (CIA)

An AI-powered agent that:

1. **Accepts carrier specifications** (API docs, credentials, features needed)
2. **Executes integration phases** following CARRIER_INTEGRATION_GUIDE.md
3. **Runs automated test loops** with failure analysis and code fixes
4. **Iterates until success** or reaches a defined iteration limit
5. **Reports final status** with detailed logs

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Karrio CLI (./bin/cli)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐    ┌──────────────────┐    ┌────────────────┐ │
│  │   studio start   │    │   agent start    │    │  agent status  │ │
│  │  (existing UI)   │    │   (new command)  │    │  (monitoring)  │ │
│  └──────────────────┘    └──────────────────┘    └────────────────┘ │
│                                   │                                  │
│                                   ▼                                  │
│           ┌───────────────────────────────────────────┐             │
│           │         Integration Agent Engine          │             │
│           ├───────────────────────────────────────────┤             │
│           │  ┌─────────────────────────────────────┐  │             │
│           │  │         Agent Orchestrator          │  │             │
│           │  │  - Phase management                 │  │             │
│           │  │  - Iteration control                │  │             │
│           │  │  - Success evaluation               │  │             │
│           │  └─────────────────────────────────────┘  │             │
│           │                    │                      │             │
│           │      ┌─────────────┴─────────────┐       │             │
│           │      ▼                           ▼       │             │
│           │  ┌────────────┐           ┌───────────┐  │             │
│           │  │  AI Core   │           │  Executor │  │             │
│           │  │ (Claude)   │◄─────────►│   (Shell) │  │             │
│           │  └────────────┘           └───────────┘  │             │
│           │      │                           │       │             │
│           │      ▼                           ▼       │             │
│           │  ┌────────────┐           ┌───────────┐  │             │
│           │  │   Skill    │           │  Result   │  │             │
│           │  │  Loader    │           │  Parser   │  │             │
│           │  └────────────┘           └───────────┘  │             │
│           └───────────────────────────────────────────┘             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Design

### 1. CLI Integration

#### New Commands

```bash
# Start an integration agent session
./bin/cli agent start \
  --carrier-slug "new_carrier" \
  --display-name "New Carrier" \
  --features "rating,shipping,tracking" \
  --api-docs "https://api.newcarrier.com/docs" \
  --path "modules/connectors" \
  --max-iterations 10 \
  --ai-provider "claude"

# Check agent status
./bin/cli agent status [session_id]

# List active/completed agent sessions
./bin/cli agent list

# Resume a paused session
./bin/cli agent resume [session_id]

# Stop an agent session
./bin/cli agent stop [session_id]

# View agent logs
./bin/cli agent logs [session_id] [--tail 100]
```

#### File Structure

```
modules/cli/karrio_cli/
├── commands/
│   ├── agent.py              # New: Agent CLI commands
│   └── ...
├── agent/
│   ├── __init__.py
│   ├── engine.py             # Core agent orchestration
│   ├── phases.py             # Phase definitions and execution
│   ├── evaluator.py          # Success criteria evaluation
│   ├── executor.py           # Shell command executor
│   ├── ai_client.py          # AI provider abstraction
│   └── session.py            # Session management
├── skills/
│   └── carrier-integration/  # Skill files (already created)
└── ...
```

### 2. Agent Phases

The agent operates in discrete phases, each with defined inputs, outputs, and success criteria:

#### Phase 1: Setup
```python
class SetupPhase:
    """Bootstrap carrier extension structure."""
    
    inputs = ["carrier_slug", "display_name", "features", "path", "is_xml_api"]
    
    actions = [
        "activate_environment",
        "run_add_extension_command",
        "verify_directory_structure",
    ]
    
    success_criteria = [
        "extension_directory_exists",
        "pyproject_toml_exists",
        "generate_script_exists",
        "schemas_directory_exists",
    ]
```

#### Phase 2: Schema Population
```python
class SchemaPopulationPhase:
    """Populate API schema samples."""
    
    inputs = ["api_docs_url", "api_examples", "carrier_path"]
    
    actions = [
        "analyze_api_documentation",
        "extract_request_response_samples",
        "determine_api_field_format",  # camelCase, snake_case, PascalCase
        "write_schema_files",
        "configure_generate_script",
    ]
    
    success_criteria = [
        "error_response_schema_exists",
        "feature_schemas_exist",  # rate_request.json, etc.
        "generate_script_configured",
    ]
```

#### Phase 3: Code Generation
```python
class CodeGenerationPhase:
    """Generate Python dataclasses from schemas."""
    
    inputs = ["carrier_path"]
    
    actions = [
        "make_generate_executable",
        "run_generate_script",
        "verify_generated_files",
    ]
    
    success_criteria = [
        "generated_python_files_exist",
        "imports_work_correctly",
        "no_syntax_errors",
    ]
```

#### Phase 4: Implementation
```python
class ImplementationPhase:
    """Implement provider logic."""
    
    inputs = ["carrier_path", "features", "api_docs"]
    
    sub_phases = [
        "configure_settings",
        "configure_utils",
        "define_units",
        "implement_proxy",
        "implement_rate_provider",
        "implement_tracking_provider",
        "implement_shipment_provider",
        "implement_error_parser",
    ]
    
    success_criteria = [
        "settings_configured",
        "utils_has_server_url",
        "units_defined",
        "proxy_methods_implemented",
        "provider_functions_use_schema_types",
    ]
```

#### Phase 5: Testing
```python
class TestingPhase:
    """Create and run tests."""
    
    inputs = ["carrier_path", "features"]
    
    actions = [
        "verify_test_fixtures",
        "update_test_data",
        "run_carrier_tests",
        "analyze_failures",
        "fix_implementation",  # Loop back if needed
    ]
    
    success_criteria = [
        "all_carrier_tests_pass",
        "sdk_tests_pass",
    ]
    
    max_fix_iterations = 5
```

#### Phase 6: Validation
```python
class ValidationPhase:
    """Final validation against all success criteria."""
    
    actions = [
        "verify_plugin_registration",
        "verify_installation",
        "run_full_test_suite",
        "generate_completion_report",
    ]
    
    success_criteria = [
        "plugin_in_list",
        "plugin_show_works",
        "pip_install_works",
        "all_tests_pass",
    ]
```

### 3. Test-Fix Iteration Loop

The agent implements an autonomous test-fix loop:

```python
class TestFixLoop:
    """Automated test failure analysis and fix cycle."""
    
    def run(self, max_iterations: int = 5) -> bool:
        for iteration in range(max_iterations):
            # Run tests
            result = self.executor.run_tests()
            
            if result.success:
                return True
            
            # Analyze failures
            analysis = self.ai_client.analyze_test_failures(
                test_output=result.output,
                carrier_path=self.carrier_path,
                implementation_files=self.get_implementation_files(),
            )
            
            # Apply fixes
            for fix in analysis.suggested_fixes:
                self.apply_fix(fix)
            
            # Log iteration
            self.log_iteration(iteration, result, analysis)
        
        return False
```

### 4. AI Client Abstraction

Support multiple AI providers:

```python
class AIClient(Protocol):
    """Abstract AI provider interface."""
    
    def analyze_api_docs(self, url: str) -> APIAnalysis:
        """Analyze carrier API documentation."""
        ...
    
    def generate_schema_samples(self, api_analysis: APIAnalysis) -> List[SchemaSample]:
        """Generate request/response schema samples."""
        ...
    
    def implement_provider(self, feature: str, schemas: Dict, context: Dict) -> str:
        """Generate provider implementation code."""
        ...
    
    def analyze_test_failures(self, output: str, files: Dict) -> FailureAnalysis:
        """Analyze test failures and suggest fixes."""
        ...
    
    def fix_code(self, file_path: str, error: str, context: Dict) -> CodeFix:
        """Generate code fix for a specific error."""
        ...


class ClaudeClient(AIClient):
    """Claude-based AI client with skill loading."""
    
    def __init__(self, api_key: str, skill_path: str):
        self.client = Anthropic(api_key=api_key)
        self.skill = self.load_skill(skill_path)
    
    def load_skill(self, path: str) -> Skill:
        """Load carrier integration skill."""
        skill_dir = Path(path)
        return Skill(
            instructions=self.load_file(skill_dir / "instructions.md"),
            examples=self.load_examples(skill_dir / "examples"),
            metadata=json.load(skill_dir / "skill.json"),
        )
```

### 5. Session Management

```python
@dataclass
class AgentSession:
    """Agent session state."""
    
    id: str
    carrier_slug: str
    display_name: str
    features: List[str]
    path: str
    status: SessionStatus  # pending, running, paused, completed, failed
    current_phase: str
    iteration: int
    max_iterations: int
    created_at: datetime
    updated_at: datetime
    logs: List[LogEntry]
    artifacts: Dict[str, str]  # Generated files
    
    def to_dict(self) -> dict:
        ...
    
    @classmethod
    def from_dict(cls, data: dict) -> "AgentSession":
        ...


class SessionManager:
    """Manage agent sessions with persistence."""
    
    sessions_dir = Path(".karrio/agent_sessions")
    
    def create(self, config: AgentConfig) -> AgentSession:
        ...
    
    def get(self, session_id: str) -> Optional[AgentSession]:
        ...
    
    def list(self, status: Optional[SessionStatus] = None) -> List[AgentSession]:
        ...
    
    def update(self, session: AgentSession) -> None:
        ...
    
    def delete(self, session_id: str) -> None:
        ...
```

### 6. Executor

```python
class Executor:
    """Execute shell commands with capture and timeout."""
    
    def __init__(self, root_dir: Path, timeout: int = 300):
        self.root_dir = root_dir
        self.timeout = timeout
    
    def run(self, command: List[str], capture: bool = True) -> ExecutionResult:
        """Run a shell command."""
        process = subprocess.run(
            command,
            cwd=self.root_dir,
            capture_output=capture,
            text=True,
            timeout=self.timeout,
        )
        return ExecutionResult(
            command=" ".join(command),
            stdout=process.stdout,
            stderr=process.stderr,
            returncode=process.returncode,
            success=process.returncode == 0,
        )
    
    def activate_env(self) -> ExecutionResult:
        """Activate Karrio development environment."""
        return self.run(["bash", "-c", "source ./bin/activate-env && echo 'OK'"])
    
    def add_extension(self, config: ExtensionConfig) -> ExecutionResult:
        """Run add-extension command."""
        cmd = [
            "./bin/cli", "sdk", "add-extension",
            "--path", config.path,
            "--carrier-slug", config.carrier_slug,
            "--display-name", config.display_name,
            "--features", ",".join(config.features),
            "--version", config.version,
            "--confirm",
        ]
        if config.is_xml_api:
            cmd.append("--is-xml-api")
        else:
            cmd.append("--no-is-xml-api")
        return self.run(cmd)
    
    def run_generate(self, carrier_path: str) -> ExecutionResult:
        """Run schema generation."""
        return self.run(["./bin/run-generate-on", carrier_path])
    
    def run_tests(self, carrier_path: str) -> ExecutionResult:
        """Run carrier tests."""
        tests_path = Path(carrier_path) / "tests"
        return self.run([
            sys.executable, "-m", "unittest",
            "discover", "-v", "-f", str(tests_path)
        ])
    
    def run_sdk_tests(self) -> ExecutionResult:
        """Run SDK tests."""
        return self.run(["./bin/run-sdk-tests"])
    
    def install_extension(self, carrier_path: str) -> ExecutionResult:
        """Install extension in editable mode."""
        return self.run(["pip", "install", "-e", carrier_path])
    
    def show_plugin(self, carrier_slug: str) -> ExecutionResult:
        """Show plugin metadata."""
        return self.run(["./bin/cli", "plugins", "show", carrier_slug])
```

### 7. Evaluator

```python
class SuccessEvaluator:
    """Evaluate success criteria."""
    
    def __init__(self, carrier_path: Path, carrier_slug: str):
        self.carrier_path = carrier_path
        self.carrier_slug = carrier_slug
    
    def evaluate_all(self) -> EvaluationReport:
        """Run all success criteria checks."""
        criteria = [
            self.check_directory_structure(),
            self.check_schema_files(),
            self.check_generated_code(),
            self.check_provider_files(),
            self.check_test_files(),
            self.check_plugin_metadata(),
            self.check_tests_pass(),
            self.check_sdk_tests_pass(),
            self.check_plugin_registration(),
            self.check_installation(),
        ]
        
        return EvaluationReport(
            passed=sum(1 for c in criteria if c.passed),
            total=len(criteria),
            criteria=criteria,
            success=all(c.passed for c in criteria),
        )
    
    def check_directory_structure(self) -> CriterionResult:
        """Verify extension directory structure."""
        required = [
            "schemas",
            "karrio/mappers",
            "karrio/providers",
            "karrio/schemas",
            "karrio/plugins",
            "tests",
        ]
        missing = [d for d in required if not (self.carrier_path / d).exists()]
        return CriterionResult(
            name="Directory Structure",
            passed=len(missing) == 0,
            message=f"Missing: {missing}" if missing else "All directories present",
        )
    
    # ... additional check methods
```

## User Experience

### Starting an Integration

```bash
# Interactive mode (prompts for details)
./bin/cli agent start --interactive

# Full specification
./bin/cli agent start \
  --carrier-slug "acme_shipping" \
  --display-name "ACME Shipping" \
  --features "rating,shipping,tracking" \
  --api-docs "https://api.acme-shipping.com/docs/v2" \
  --api-key "$ACME_API_KEY" \
  --path "modules/connectors" \
  --max-iterations 10

# From specification file
./bin/cli agent start --config ./carrier_specs/acme_shipping.yaml
```

### Monitoring Progress

```bash
# Watch live progress
./bin/cli agent status abc123 --watch

# Output:
# Session: abc123
# Carrier: ACME Shipping (acme_shipping)
# Status: running
# Phase: Testing (4/6)
# Iteration: 3/10
# 
# Progress:
# ✅ Setup - Complete
# ✅ Schema Population - Complete
# ✅ Code Generation - Complete
# 🔄 Implementation - In Progress (fixing rate.py)
# ⏳ Testing - Pending
# ⏳ Validation - Pending
# 
# Recent Activity:
# [10:45:23] Running carrier tests...
# [10:45:25] 2 tests failed: test_parse_rate_response, test_get_rates
# [10:45:26] Analyzing failures...
# [10:45:30] Applying fix to rate.py (line 45)
```

### Viewing Logs

```bash
./bin/cli agent logs abc123 --tail 50

# Output:
# [2024-01-18 10:45:23] INFO  Phase: Testing
# [2024-01-18 10:45:23] INFO  Running: python -m unittest discover -v -f modules/connectors/acme_shipping/tests
# [2024-01-18 10:45:25] ERROR test_parse_rate_response (tests.acme_shipping.test_rate.TestAcmeShippingRating)
# [2024-01-18 10:45:25] ERROR AssertionError: Lists differ: [] != [{'carrier_id': 'acme_shipping'...
# [2024-01-18 10:45:26] INFO  Analyzing test failure...
# [2024-01-18 10:45:30] INFO  Fix identified: rate.py line 45 - incorrect response path
# [2024-01-18 10:45:30] INFO  Applying fix...
```

### Completion Report

```bash
./bin/cli agent report abc123

# Output:
# ═══════════════════════════════════════════════════════════════
#                    Integration Report: ACME Shipping
# ═══════════════════════════════════════════════════════════════
# 
# Status: ✅ SUCCESS
# Duration: 12m 34s
# Iterations: 4
# 
# Success Criteria:
# ✅ Extension scaffolded
# ✅ Schema samples created (5 files)
# ✅ Code generation successful (8 Python files)
# ✅ Settings configured
# ✅ Units defined (12 services, 8 options)
# ✅ Proxy implemented (3 methods)
# ✅ Provider functions implemented
# ✅ All carrier tests pass (12/12)
# ✅ SDK tests pass
# ✅ Plugin registered
# ✅ Installation verified
# 
# Generated Files:
# - modules/connectors/acme_shipping/
#   ├── karrio/mappers/acme_shipping/ (4 files)
#   ├── karrio/providers/acme_shipping/ (6 files)
#   ├── karrio/schemas/acme_shipping/ (8 files)
#   ├── karrio/plugins/acme_shipping/ (1 file)
#   ├── schemas/ (5 files)
#   └── tests/acme_shipping/ (4 files)
# 
# Next Steps:
# 1. Review generated code in modules/connectors/acme_shipping/
# 2. Test with real API credentials
# 3. Add additional test cases for edge cases
# 4. Submit for code review
```

## Configuration

### Agent Configuration File

```yaml
# .karrio/agent.yaml

defaults:
  ai_provider: claude
  max_iterations: 10
  timeout_seconds: 300
  
claude:
  model: claude-sonnet-4-20250514
  skill_path: modules/cli/karrio_cli/skills/carrier-integration
  
logging:
  level: INFO
  file: .karrio/agent_sessions/{session_id}/agent.log
  
persistence:
  sessions_dir: .karrio/agent_sessions
  retention_days: 30
```

### Carrier Specification File

```yaml
# carrier_specs/acme_shipping.yaml

carrier:
  slug: acme_shipping
  display_name: ACME Shipping
  website: https://www.acme-shipping.com

api:
  type: json  # or xml
  base_url: https://api.acme-shipping.com/v2
  sandbox_url: https://sandbox.acme-shipping.com/v2
  docs_url: https://api.acme-shipping.com/docs
  auth_type: api_key  # or oauth, basic

features:
  - rating
  - shipping
  - tracking

credentials:
  # Reference to environment variables
  api_key: $ACME_API_KEY
  account_number: $ACME_ACCOUNT

settings:
  path: modules/connectors
  version: "2025.1"
  max_iterations: 10
```

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

1. **CLI Commands**
   - Implement `agent start`, `status`, `list`, `stop` commands
   - Session management with file-based persistence

2. **Executor**
   - Shell command execution with capture
   - Timeout handling
   - Environment activation

3. **Basic Orchestration**
   - Phase sequencing
   - Success/failure tracking

### Phase 2: AI Integration (Week 3-4)

1. **AI Client**
   - Claude API integration
   - Skill loading
   - Prompt templates

2. **Analysis Capabilities**
   - Test failure analysis
   - Code fix generation
   - API documentation parsing

### Phase 3: Test-Fix Loop (Week 5-6)

1. **Iteration Engine**
   - Test execution
   - Failure parsing
   - Fix application

2. **Evaluator**
   - Success criteria checks
   - Progress tracking
   - Report generation

### Phase 4: Polish & Documentation (Week 7-8)

1. **Error Handling**
   - Graceful failures
   - Resume capability
   - Manual intervention points

2. **Documentation**
   - User guide
   - Troubleshooting guide
   - API reference

## Success Metrics

1. **Automation Rate**: % of integrations completed without manual intervention
2. **Iteration Efficiency**: Average iterations to success
3. **Time Savings**: Time compared to manual development
4. **Quality**: Test coverage and code review feedback

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI generates incorrect code | High | Strong skill instructions, validation checks, iteration limits |
| Infinite fix loops | Medium | Max iteration limits, divergence detection |
| API changes break agent | Medium | Modular phase design, easy updates |
| Cost of AI API calls | Low | Caching, efficient prompts, local model option |

## Future Enhancements

1. **Multi-carrier batch processing**
2. **Learning from successful integrations**
3. **Integration with GitHub PRs**
4. **Real API testing (with credentials)**
5. **Custom skill creation UI**
6. **Local LLM support (Ollama, etc.)**

## Appendix: Related Files

- `CARRIER_INTEGRATION_GUIDE.md` - Integration guide the agent follows
- `modules/cli/karrio_cli/skills/carrier-integration/` - Claude skill files
- `modules/cli/karrio_cli/commands/studio.py` - Existing studio implementation
- `modules/cli/karrio_cli/templates/` - Code generation templates
