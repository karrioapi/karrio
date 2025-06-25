"""
RAG (Retrieval-Augmented Generation) System for Karrio Carrier Integration

This module provides semantic search and pattern extraction capabilities
for analyzing existing Karrio connectors and SDK components.
"""

import os
import json
import typing
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
import hashlib


@dataclass
class CodeFragment:
    """Represents a fragment of code with metadata."""
    file_path: str
    content: str
    start_line: int
    end_line: int
    fragment_type: str  # 'class', 'function', 'import', 'comment'
    context: str
    embedding_hash: Optional[str] = None


@dataclass
class ConnectorPattern:
    """Extracted pattern from existing connectors."""
    pattern_type: str  # 'auth', 'mapping', 'schema', 'error_handling'
    carrier_name: str
    description: str
    code_example: str
    usage_context: str
    related_files: List[str]
    confidence_score: float = 0.0


class KarrioRAGSystem:
    """RAG system for Karrio connector analysis and pattern extraction."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()  # Ensure we have absolute path
        self.connectors_dir = self.workspace_root / "modules" / "connectors"
        self.sdk_dir = self.workspace_root / "modules" / "sdk"
        self.templates_dir = self.workspace_root / "modules" / "cli" / "karrio_cli" / "templates"

        # In-memory knowledge base
        self.code_fragments: List[CodeFragment] = []
        self.patterns: List[ConnectorPattern] = []
        self.indexed_files: Dict[str, str] = {}  # file_path -> content_hash

        # Initialize the knowledge base
        self._build_knowledge_base()

    def _build_knowledge_base(self):
        """Build the knowledge base by indexing existing connectors and SDK."""
        print("Building RAG knowledge base...")
        print(f"Workspace root: {self.workspace_root}")
        print(f"Connectors dir: {self.connectors_dir} (exists: {self.connectors_dir.exists()})")
        print(f"SDK dir: {self.sdk_dir} (exists: {self.sdk_dir.exists()})")

        # Index connector implementations
        self._index_connectors()

        # Index SDK patterns
        self._index_sdk()

        # Index CLI templates
        self._index_templates()

        # Extract common patterns
        self._extract_patterns()

        print(f"Knowledge base built with {len(self.code_fragments)} fragments and {len(self.patterns)} patterns")

    def _index_connectors(self):
        """Index all existing connector implementations."""
        if not self.connectors_dir.exists():
            return

        for carrier_dir in self.connectors_dir.iterdir():
            if carrier_dir.is_dir() and not carrier_dir.name.startswith('.'):
                self._index_connector(carrier_dir)

    def _index_connector(self, carrier_dir: Path):
        """Index a specific connector directory."""
        carrier_name = carrier_dir.name

        # Index Python files
        for py_file in carrier_dir.rglob("*.py"):
            if py_file.is_file():
                self._index_python_file(py_file, carrier_name)

        # Index configuration files
        for config_file in carrier_dir.glob("*.toml"):
            if config_file.is_file():
                self._index_config_file(config_file, carrier_name)

    def _index_python_file(self, file_path: Path, context: str):
        """Index a Python file and extract code fragments."""
        try:
            content = file_path.read_text(encoding='utf-8')
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Skip if already indexed and unchanged
            file_key = str(file_path)
            if file_key in self.indexed_files and self.indexed_files[file_key] == content_hash:
                return

            self.indexed_files[file_key] = content_hash

            # Extract different types of code fragments
            fragments = self._extract_code_fragments(file_path, content, context)
            self.code_fragments.extend(fragments)

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def _extract_code_fragments(self, file_path: Path, content: str, context: str) -> List[CodeFragment]:
        """Extract meaningful code fragments from Python content."""
        fragments = []
        lines = content.split('\n')

        # Extract imports
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                fragments.append(CodeFragment(
                    file_path=str(file_path),
                    content=line.strip(),
                    start_line=i + 1,
                    end_line=i + 1,
                    fragment_type='import',
                    context=context
                ))

        # Extract class definitions
        fragments.extend(self._extract_classes(file_path, content, context))

        # Extract function definitions
        fragments.extend(self._extract_functions(file_path, content, context))

        return fragments

    def _extract_classes(self, file_path: Path, content: str, context: str) -> List[CodeFragment]:
        """Extract class definitions and their methods."""
        fragments = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith('class '):
                # Find the end of the class
                class_start = i
                indent_level = len(line) - len(line.lstrip())

                j = i + 1
                while j < len(lines):
                    if lines[j].strip() and (len(lines[j]) - len(lines[j].lstrip())) <= indent_level:
                        if not lines[j].strip().startswith(('"""', "'''")):
                            break
                    j += 1

                class_content = '\n'.join(lines[class_start:j])
                fragments.append(CodeFragment(
                    file_path=str(file_path),
                    content=class_content,
                    start_line=class_start + 1,
                    end_line=j,
                    fragment_type='class',
                    context=context
                ))

                i = j
            else:
                i += 1

        return fragments

    def _extract_functions(self, file_path: Path, content: str, context: str) -> List[CodeFragment]:
        """Extract function definitions."""
        fragments = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith('def '):
                # Find the end of the function
                func_start = i
                indent_level = len(line) - len(line.lstrip())

                j = i + 1
                while j < len(lines):
                    if lines[j].strip() and (len(lines[j]) - len(lines[j].lstrip())) <= indent_level:
                        break
                    j += 1

                func_content = '\n'.join(lines[func_start:j])
                fragments.append(CodeFragment(
                    file_path=str(file_path),
                    content=func_content,
                    start_line=func_start + 1,
                    end_line=j,
                    fragment_type='function',
                    context=context
                ))

                i = j
            else:
                i += 1

        return fragments

    def _index_config_file(self, file_path: Path, context: str):
        """Index configuration files."""
        try:
            content = file_path.read_text(encoding='utf-8')
            self.code_fragments.append(CodeFragment(
                file_path=str(file_path),
                content=content,
                start_line=1,
                end_line=len(content.split('\n')),
                fragment_type='config',
                context=context
            ))
        except Exception as e:
            print(f"Error indexing config {file_path}: {e}")

    def _index_sdk(self):
        """Index SDK patterns and utilities."""
        if not self.sdk_dir.exists():
            return

        for py_file in self.sdk_dir.rglob("*.py"):
            if py_file.is_file():
                self._index_python_file(py_file, "sdk")

    def _index_templates(self):
        """Index CLI templates."""
        if not self.templates_dir.exists():
            return

        for template_file in self.templates_dir.glob("*.py"):
            if template_file.is_file():
                self._index_python_file(template_file, "template")

    def _extract_patterns(self):
        """Extract common patterns from indexed code fragments."""
        # Group fragments by functionality
        auth_patterns = self._find_auth_patterns()
        mapping_patterns = self._find_mapping_patterns()
        schema_patterns = self._find_schema_patterns()
        error_patterns = self._find_error_patterns()

        self.patterns.extend(auth_patterns)
        self.patterns.extend(mapping_patterns)
        self.patterns.extend(schema_patterns)
        self.patterns.extend(error_patterns)

    def _find_auth_patterns(self) -> List[ConnectorPattern]:
        """Find authentication patterns across connectors."""
        patterns = []

        # Look for authentication-related code
        auth_keywords = ['auth', 'token', 'api_key', 'credential', 'login', 'bearer', 'oauth']

        for fragment in self.code_fragments:
            if any(keyword in fragment.content.lower() for keyword in auth_keywords):
                if fragment.fragment_type in ['function', 'class']:
                    patterns.append(ConnectorPattern(
                        pattern_type='auth',
                        carrier_name=fragment.context,
                        description=f"Authentication pattern from {fragment.context}",
                        code_example=fragment.content,
                        usage_context=f"Lines {fragment.start_line}-{fragment.end_line} in {fragment.file_path}",
                        related_files=[fragment.file_path],
                        confidence_score=0.8
                    ))

        return patterns

    def _find_mapping_patterns(self) -> List[ConnectorPattern]:
        """Find mapping patterns across connectors."""
        patterns = []

        # Look for mapping-related functions
        mapping_keywords = ['parse_', 'request', 'response', 'transform', 'map_', 'convert']

        for fragment in self.code_fragments:
            if fragment.fragment_type == 'function':
                if any(keyword in fragment.content.lower() for keyword in mapping_keywords):
                    patterns.append(ConnectorPattern(
                        pattern_type='mapping',
                        carrier_name=fragment.context,
                        description=f"Mapping pattern from {fragment.context}",
                        code_example=fragment.content,
                        usage_context=f"Lines {fragment.start_line}-{fragment.end_line} in {fragment.file_path}",
                        related_files=[fragment.file_path],
                        confidence_score=0.7
                    ))

        return patterns

    def _find_schema_patterns(self) -> List[ConnectorPattern]:
        """Find schema patterns across connectors."""
        patterns = []

        # Look for schema-related classes
        schema_keywords = ['@attr.s', 'class.*Type:', 'dataclass', 'jstruct']

        for fragment in self.code_fragments:
            if fragment.fragment_type == 'class':
                if any(keyword.lower() in fragment.content.lower() for keyword in schema_keywords):
                    patterns.append(ConnectorPattern(
                        pattern_type='schema',
                        carrier_name=fragment.context,
                        description=f"Schema pattern from {fragment.context}",
                        code_example=fragment.content,
                        usage_context=f"Lines {fragment.start_line}-{fragment.end_line} in {fragment.file_path}",
                        related_files=[fragment.file_path],
                        confidence_score=0.9
                    ))

        return patterns

    def _find_error_patterns(self) -> List[ConnectorPattern]:
        """Find error handling patterns across connectors."""
        patterns = []

        # Look for error handling code
        error_keywords = ['error', 'exception', 'message', 'parse_error', 'handle_error']

        for fragment in self.code_fragments:
            if any(keyword in fragment.content.lower() for keyword in error_keywords):
                if fragment.fragment_type in ['function', 'class']:
                    patterns.append(ConnectorPattern(
                        pattern_type='error_handling',
                        carrier_name=fragment.context,
                        description=f"Error handling pattern from {fragment.context}",
                        code_example=fragment.content,
                        usage_context=f"Lines {fragment.start_line}-{fragment.end_line} in {fragment.file_path}",
                        related_files=[fragment.file_path],
                        confidence_score=0.6
                    ))

        return patterns

    def search_patterns(self,
                       pattern_type: Optional[str] = None,
                       carrier_name: Optional[str] = None,
                       keywords: Optional[List[str]] = None,
                       limit: int = 10) -> List[ConnectorPattern]:
        """Search for patterns based on criteria."""
        filtered_patterns = self.patterns

        # Filter by pattern type
        if pattern_type:
            filtered_patterns = [p for p in filtered_patterns if p.pattern_type == pattern_type]

        # Filter by carrier name
        if carrier_name:
            filtered_patterns = [p for p in filtered_patterns if carrier_name.lower() in p.carrier_name.lower()]

        # Filter by keywords
        if keywords:
            def matches_keywords(pattern: ConnectorPattern) -> bool:
                text = f"{pattern.description} {pattern.code_example}".lower()
                return any(keyword.lower() in text for keyword in keywords)

            filtered_patterns = [p for p in filtered_patterns if matches_keywords(p)]

        # Sort by confidence score
        filtered_patterns.sort(key=lambda p: p.confidence_score, reverse=True)

        return filtered_patterns[:limit]

    def get_similar_carriers(self, carrier_characteristics: Dict[str, Any]) -> List[str]:
        """Find carriers with similar characteristics."""
        # Simple similarity based on common patterns
        api_type = carrier_characteristics.get('api_type', 'REST')
        auth_type = carrier_characteristics.get('auth_type', 'API_KEY')
        operations = set(carrier_characteristics.get('operations', []))

        similar_carriers = []
        carrier_scores = {}

        for pattern in self.patterns:
            carrier = pattern.carrier_name
            if carrier not in carrier_scores:
                carrier_scores[carrier] = 0

            # Score based on pattern matches
            if api_type.lower() in pattern.code_example.lower():
                carrier_scores[carrier] += 1

            if auth_type.lower() in pattern.code_example.lower():
                carrier_scores[carrier] += 2

            # Check for operation matches
            for op in operations:
                if op.lower() in pattern.code_example.lower():
                    carrier_scores[carrier] += 1

        # Sort by score and return top carriers
        sorted_carriers = sorted(carrier_scores.items(), key=lambda x: x[1], reverse=True)
        return [carrier for carrier, score in sorted_carriers[:5] if score > 0]

    def get_implementation_examples(self,
                                  operation: str,
                                  carrier_names: List[str] = None) -> List[CodeFragment]:
        """Get implementation examples for specific operations."""
        examples = []

        for fragment in self.code_fragments:
            if operation.lower() in fragment.content.lower():
                if carrier_names is None or fragment.context in carrier_names:
                    examples.append(fragment)

        return examples[:10]  # Limit results

    def analyze_carrier_structure(self, carrier_name: str) -> Dict[str, Any]:
        """Analyze the structure of an existing carrier implementation."""
        analysis = {
            'carrier_name': carrier_name,
            'files': [],
            'patterns': [],
            'structure': {
                'has_schemas': False,
                'has_mappings': False,
                'has_tests': False,
                'has_providers': False
            }
        }

        # Find all fragments for this carrier
        carrier_fragments = [f for f in self.code_fragments if f.context == carrier_name]

        for fragment in carrier_fragments:
            analysis['files'].append({
                'path': fragment.file_path,
                'type': fragment.fragment_type,
                'lines': f"{fragment.start_line}-{fragment.end_line}"
            })

            # Determine structure components
            if 'schemas' in fragment.file_path:
                analysis['structure']['has_schemas'] = True
            elif 'mappers' in fragment.file_path:
                analysis['structure']['has_mappings'] = True
            elif 'test' in fragment.file_path:
                analysis['structure']['has_tests'] = True
            elif 'providers' in fragment.file_path:
                analysis['structure']['has_providers'] = True

        # Find patterns for this carrier
        analysis['patterns'] = [p for p in self.patterns if p.carrier_name == carrier_name]

        return analysis


# Global RAG system instance
_rag_system: Optional[KarrioRAGSystem] = None


def get_rag_system(workspace_root: Path) -> KarrioRAGSystem:
    """Get or create the global RAG system instance."""
    global _rag_system
    if _rag_system is None:
        _rag_system = KarrioRAGSystem(workspace_root)
    return _rag_system


def search_implementation_patterns(pattern_type: str,
                                 carrier_name: str = None,
                                 keywords: List[str] = None) -> List[Dict[str, Any]]:
    """Search for implementation patterns using the RAG system."""
    from pathlib import Path

    # Get workspace root - resolve relative to this file's location
    workspace_root = Path(__file__).resolve().parents[5]  # Use resolve() for consistent path handling
    rag = get_rag_system(workspace_root)

    patterns = rag.search_patterns(
        pattern_type=pattern_type,
        carrier_name=carrier_name,
        keywords=keywords
    )

    return [
        {
            'pattern_type': p.pattern_type,
            'carrier_name': p.carrier_name,
            'description': p.description,
            'code_example': p.code_example,
            'usage_context': p.usage_context,
            'confidence_score': p.confidence_score
        }
        for p in patterns
    ]
