"""
Code quality auditing tool for checking adherence to SOLID principles and best practices.
This script analyzes the codebase and reports on potential issues.
"""
import os
import re
import sys
import importlib
import inspect
from abc import ABC
from collections import defaultdict
from typing import List, Dict, Tuple, Set, Any


class CodeQualityAuditor:
    """Analyzes code for adherence to SOLID principles and best practices."""
    
    def __init__(self, project_root: str):
        """
        Initialize the auditor with the project root directory.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = project_root
        self.modules = []
        self.issues = []
    
    def scan_directory(self, directory: str, exclude_dirs: List[str] = None) -> None:
        """
        Scan a directory for Python files and collect modules.
        
        Args:
            directory: Directory to scan
            exclude_dirs: Directories to exclude from scanning
        """
        if exclude_dirs is None:
            exclude_dirs = ['venv', '__pycache__', '.git']
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)
                    self.modules.append(rel_path)
    
    def audit_code(self) -> List[Dict[str, Any]]:
        """
        Perform a code quality audit and return issues.
        
        Returns:
            List of issues found in the codebase
        """
        self.issues = []
        
        # SRP - Single Responsibility Principle
        self._check_single_responsibility()
        
        # OCP - Open/Closed Principle
        self._check_open_closed()
        
        # LSP - Liskov Substitution Principle
        self._check_liskov_substitution()
        
        # ISP - Interface Segregation Principle
        self._check_interface_segregation()
        
        # DIP - Dependency Inversion Principle
        self._check_dependency_inversion()
        
        # Check general best practices
        self._check_best_practices()
        
        return self.issues
    
    def _check_single_responsibility(self) -> None:
        """Check for violations of the Single Responsibility Principle."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Look for classes with too many methods or too many lines
            class_matches = re.finditer(r'class\s+(\w+)', content)
            for match in class_matches:
                class_name = match.group(1)
                class_code = self._extract_class_code(content, class_name)
                
                # Check method count
                method_count = len(re.findall(r'def\s+\w+\(', class_code))
                if method_count > 10:
                    self.issues.append({
                        'principle': 'SRP',
                        'file': module_path,
                        'class': class_name,
                        'description': f'Class has {method_count} methods, which might violate SRP'
                    })
                
                # Check line count
                line_count = class_code.count('\n')
                if line_count > 100:
                    self.issues.append({
                        'principle': 'SRP',
                        'file': module_path,
                        'class': class_name,
                        'description': f'Class has {line_count} lines, which might be too complex for SRP'
                    })
    
    def _check_open_closed(self) -> None:
        """Check for potential violations of the Open/Closed Principle."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Look for if-else chains with type checks (often an OCP violation)
            if_type_chains = re.findall(r'if\s+isinstance\(.*\).*\n.*elif\s+isinstance\(', content)
            if if_type_chains:
                self.issues.append({
                    'principle': 'OCP',
                    'file': module_path,
                    'description': 'Code contains type-checking if-else chains, which often violate OCP'
                })
    
    def _check_liskov_substitution(self) -> None:
        """Check for potential violations of the Liskov Substitution Principle."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Look for overridden methods that might violate contracts
            # For example, raising NotImplementedError
            not_implemented = re.findall(r'def\s+\w+\(.*\).*\n.*raise\s+NotImplementedError', content)
            if not_implemented:
                self.issues.append({
                    'principle': 'LSP',
                    'file': module_path,
                    'description': 'Code contains methods that raise NotImplementedError, which might violate LSP'
                })
    
    def _check_interface_segregation(self) -> None:
        """Check for potential violations of the Interface Segregation Principle."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Look for abstract classes with too many abstract methods
            if 'ABC' in content and 'abstractmethod' in content:
                class_matches = re.finditer(r'class\s+(\w+)', content)
                for match in class_matches:
                    class_name = match.group(1)
                    class_code = self._extract_class_code(content, class_name)
                    
                    # Count abstract methods
                    abstract_method_count = class_code.count('@abstractmethod')
                    if abstract_method_count > 5:
                        self.issues.append({
                            'principle': 'ISP',
                            'file': module_path,
                            'class': class_name,
                            'description': f'Interface has {abstract_method_count} abstract methods, '
                                          f'which might violate ISP'
                        })
    
    def _check_dependency_inversion(self) -> None:
        """Check for potential violations of the Dependency Inversion Principle."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Look for direct instantiations of concrete classes
            class_names = [m.group(1) for m in re.finditer(r'class\s+(\w+)', content)]
            for class_name in class_names:
                # Skip abstract classes and interfaces
                if f"class {class_name}(ABC)" in content or f"class {class_name}(Interface)" in content:
                    continue
                
                # Check for instantiations outside the class itself
                for other_class in class_names:
                    if other_class != class_name:
                        other_class_code = self._extract_class_code(content, other_class)
                        if f"{class_name}(" in other_class_code:
                            self.issues.append({
                                'principle': 'DIP',
                                'file': module_path,
                                'class': other_class,
                                'description': f'Class directly instantiates {class_name}, '
                                              f'which might violate DIP'
                            })
    
    def _check_best_practices(self) -> None:
        """Check for adherence to general best practices."""
        for module_path in self.modules:
            with open(os.path.join(self.project_root, module_path), 'r') as f:
                content = f.read()
            
            # Check for docstrings
            class_matches = re.finditer(r'class\s+(\w+)', content)
            for match in class_matches:
                class_name = match.group(1)
                class_code = self._extract_class_code(content, class_name)
                
                # Check if class has a docstring
                if not re.search(r'class\s+\w+.*:\s*\n\s*("""|\'\'\').*("""|\'\'\').', class_code, re.DOTALL):
                    self.issues.append({
                        'principle': 'Documentation',
                        'file': module_path,
                        'class': class_name,
                        'description': 'Class is missing a docstring'
                    })
                
                # Check methods for docstrings
                method_matches = re.finditer(r'def\s+(\w+)\(', class_code)
                for method_match in method_matches:
                    method_name = method_match.group(1)
                    if method_name.startswith('__') and method_name.endswith('__'):
                        continue  # Skip dunder methods
                    
                    # Check if the method has a docstring
                    method_pos = method_match.start()
                    next_lines = class_code[method_pos:method_pos+500] # Увеличим размер проверяемого блока
                    if not re.search(r'def\s+\w+.*:\s*\n\s*("""|\'\'\')', next_lines):
                        self.issues.append({
                            'principle': 'Documentation',
                            'file': module_path,
                            'class': f"{class_name}.{method_name}",
                            'description': 'Method is missing a docstring'
                        })
    
    def _extract_class_code(self, content: str, class_name: str) -> str:
        """
        Extract the code for a specific class from a file content.
        
        Args:
            content: File content
            class_name: Name of the class to extract
            
        Returns:
            Code of the specified class
        """
        pattern = rf'class\s+{class_name}\s*(\([^)]*\))?\s*:'
        match = re.search(pattern, content)
        if not match:
            return ""
        
        start_pos = match.start()
        
        # Find the end of the class by tracking indentation
        lines = content[start_pos:].split('\n')
        class_def_indent = len(lines[0]) - len(lines[0].lstrip())
        
        end_line = 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() and len(line) - len(line.lstrip()) <= class_def_indent:
                end_line = i
                break
        
        return '\n'.join(lines[:end_line])


def main():
    """Main function to run the code quality audit."""
    if len(sys.argv) < 2:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        project_root = sys.argv[1]
    
    auditor = CodeQualityAuditor(project_root)
    
    # Scan relevant directories
    for directory in ['backend', 'ai_integration', 'data_layer']:
        dir_path = os.path.join(project_root, directory)
        if os.path.exists(dir_path):
            auditor.scan_directory(dir_path)
    
    # Perform audit
    issues = auditor.audit_code()
    
    # Report issues
    print(f"Code Quality Audit Report - {len(issues)} potential issues found")
    print("=" * 80)
    
    if not issues:
        print("No issues found. The codebase adheres well to SOLID principles!")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['principle']} Issue:")
            print(f"   File: {issue['file']}")
            if 'class' in issue:
                print(f"   Class/Method: {issue['class']}")
            print(f"   Description: {issue['description']}")
            print()


if __name__ == "__main__":
    main()
