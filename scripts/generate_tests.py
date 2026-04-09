#!/usr/bin/env python3
"""
Test Generation Script for TEQUMSA
Following Product Development team patterns from Anthropic
Auto-generates comprehensive tests for components
"""

import os
import sys
import ast
import argparse
from pathlib import Path
from typing import List, Dict, Any
import textwrap


class TestGenerator:
    """Generate comprehensive tests following Claude Code patterns"""
    
    def __init__(self):
        self.test_templates = {
            'api_endpoint': self.generate_api_test,
            'function': self.generate_function_test,
            'class': self.generate_class_test,
            'integration': self.generate_integration_test
        }
    
    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Python file to extract testable components"""
        if not file_path.exists():
            return {}
        
        content = file_path.read_text()
        try:
            tree = ast.parse(content)
        except SyntaxError:
            print(f"⚠️  Could not parse {file_path}")
            return {}
        
        analysis = {
            'functions': [],
            'classes': [],
            'api_endpoints': [],
            'imports': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if it's a Flask route
                if any(hasattr(decorator, 'attr') and 
                      decorator.attr in ['route', 'get', 'post', 'put', 'delete'] 
                      for decorator in node.decorator_list if hasattr(decorator, 'attr')):
                    analysis['api_endpoints'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                else:
                    analysis['functions'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'returns': hasattr(node, 'returns')
                    })
            
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                analysis['classes'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': methods
                })
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis['imports'].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        analysis['imports'].append(f"{node.module}.{alias.name}")
        
        return analysis
    
    def generate_api_test(self, component: Dict[str, Any], file_path: Path) -> str:
        """Generate API endpoint tests"""
        endpoint_name = component['name']
        
        test_content = f'''
    def test_{endpoint_name}_success(self, client):
        """Test successful {endpoint_name} endpoint"""
        # TODO: Add appropriate test data
        response = client.get('/{endpoint_name}')  # Adjust method and path
        assert response.status_code == 200
        # TODO: Add response validation
    
    def test_{endpoint_name}_invalid_input(self, client):
        """Test {endpoint_name} with invalid input"""
        # TODO: Add invalid input test cases
        response = client.post('/{endpoint_name}', data='invalid')
        assert response.status_code in [400, 422]
    
    def test_{endpoint_name}_error_handling(self, client):
        """Test {endpoint_name} error handling"""
        # TODO: Mock external dependencies to test error scenarios
        with patch('external_service.method') as mock_service:
            mock_service.side_effect = Exception("Service error")
            response = client.get('/{endpoint_name}')
            # Verify graceful error handling
            assert response.status_code in [500, 503]
'''
        return test_content
    
    def generate_function_test(self, component: Dict[str, Any], file_path: Path) -> str:
        """Generate function tests"""
        func_name = component['name']
        func_args = component.get('args', [])
        
        # Skip test functions and private functions
        if func_name.startswith('test_') or func_name.startswith('_'):
            return ""
        
        test_content = f'''
    def test_{func_name}_basic_functionality(self):
        """Test basic functionality of {func_name}"""
        # TODO: Add test with valid inputs
        # result = {func_name}({', '.join(['test_param'] * len(func_args))})
        # assert result is not None
        # TODO: Add specific assertions based on expected behavior
        pass
    
    def test_{func_name}_edge_cases(self):
        """Test edge cases for {func_name}"""
        # TODO: Test edge cases like empty inputs, None values, etc.
        # Test with None
        # Test with empty values
        # Test with boundary values
        pass
    
    def test_{func_name}_error_handling(self):
        """Test error handling in {func_name}"""
        # TODO: Test error scenarios
        # with pytest.raises(ExpectedError):
        #     {func_name}(invalid_input)
        pass
'''
        return test_content
    
    def generate_class_test(self, component: Dict[str, Any], file_path: Path) -> str:
        """Generate class tests"""
        class_name = component['name']
        methods = component.get('methods', [])
        
        test_content = f'''
class Test{class_name}:
    """Test cases for {class_name} class"""
    
    def test_{class_name.lower()}_initialization(self):
        """Test {class_name} initialization"""
        # TODO: Test object creation
        # obj = {class_name}()
        # assert obj is not None
        pass
'''
        
        # Add tests for each method
        for method in methods:
            if not method.startswith('_') or method == '__init__':
                test_content += f'''
    def test_{method}(self):
        """Test {class_name}.{method}"""
        # TODO: Test {method} functionality
        # obj = {class_name}()
        # result = obj.{method}()
        # assert result is not None
        pass
'''
        
        return test_content
    
    def generate_integration_test(self, components: List[Dict], file_path: Path) -> str:
        """Generate integration tests"""
        test_content = '''
class TestIntegration:
    """Integration tests for component interactions"""
    
    def test_api_frontend_integration(self):
        """Test API and frontend integration"""
        # TODO: Test full request/response cycle
        pass
    
    def test_external_service_integration(self):
        """Test integration with external services"""
        # TODO: Test OpenAI, ElevenLabs, etc. integration
        pass
    
    def test_error_propagation(self):
        """Test error handling across components"""
        # TODO: Test how errors propagate through the system
        pass
'''
        return test_content
    
    def generate_test_file(self, source_file: Path, output_dir: Path) -> Path:
        """Generate complete test file for a source file"""
        analysis = self.analyze_python_file(source_file)
        
        if not any(analysis.values()):
            print(f"⚠️  No testable components found in {source_file}")
            return None
        
        # Generate test file name
        test_file_name = f"test_{source_file.stem}.py"
        test_file_path = output_dir / test_file_name
        
        # Generate test file header
        header = f'''"""
Generated tests for {source_file.name}
Created using Claude Code test generation patterns
Following Anthropic's Product Development methodology

Auto-generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source file: {source_file}

TODO: Review and customize generated tests
TODO: Add appropriate test data and assertions
TODO: Mock external dependencies where needed
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the module being tested
try:
    from {source_file.stem} import *
except ImportError as e:
    pytest.skip(f"Could not import {source_file.stem}: {{e}}", allow_module_level=True)


@pytest.fixture
def mock_environment():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {{
        'OPENAI_API_KEY': 'test-key',
        'ELEVENLABS_API_KEY': 'test-key',
        'ALLOWED_ORIGINS': 'http://localhost:3000'
    }}):
        yield


'''
        
        # Generate test classes and functions
        test_content = header
        
        # Add tests for API endpoints
        if analysis['api_endpoints']:
            test_content += "\nclass TestAPIEndpoints:\n"
            test_content += '    """Test API endpoint functionality"""\n'
            for endpoint in analysis['api_endpoints']:
                test_content += self.generate_api_test(endpoint, source_file)
        
        # Add tests for functions
        if analysis['functions']:
            test_content += "\nclass TestFunctions:\n"
            test_content += '    """Test individual function functionality"""\n'
            for function in analysis['functions']:
                test_content += self.generate_function_test(function, source_file)
        
        # Add tests for classes
        for class_info in analysis['classes']:
            test_content += self.generate_class_test(class_info, source_file)
        
        # Add integration tests
        if analysis['api_endpoints'] or analysis['functions']:
            test_content += self.generate_integration_test(
                analysis['api_endpoints'] + analysis['functions'], 
                source_file
            )
        
        # Write test file
        test_file_path.write_text(test_content)
        print(f"✅ Generated test file: {test_file_path}")
        
        return test_file_path
    
    def generate_tests_for_directory(self, source_dir: Path, output_dir: Path):
        """Generate tests for all Python files in a directory"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        python_files = list(source_dir.glob("*.py"))
        generated_files = []
        
        for py_file in python_files:
            if py_file.name.startswith('test_'):
                continue  # Skip existing test files
            
            test_file = self.generate_test_file(py_file, output_dir)
            if test_file:
                generated_files.append(test_file)
        
        return generated_files


def main():
    """Main test generation function"""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive tests following Claude Code patterns"
    )
    parser.add_argument(
        '--component', 
        help='Specific file or component to generate tests for'
    )
    parser.add_argument(
        '--feature',
        help='Feature name for organizing tests'
    )
    parser.add_argument(
        '--output-dir',
        default='tests/generated',
        help='Output directory for generated tests'
    )
    parser.add_argument(
        '--integration-only',
        action='store_true',
        help='Generate only integration tests'
    )
    
    args = parser.parse_args()
    
    generator = TestGenerator()
    output_dir = Path(args.output_dir)
    
    print("🧪 Generating tests using Claude Code patterns...")
    
    if args.component:
        # Generate tests for specific component
        source_file = Path(args.component)
        if source_file.exists():
            generator.generate_test_file(source_file, output_dir)
        else:
            print(f"❌ File not found: {source_file}")
            return 1
    
    elif args.feature:
        # Generate tests for a feature (search for related files)
        feature_files = []
        for pattern in [f"*{args.feature}*", f"*/{args.feature}*"]:
            feature_files.extend(Path(".").glob(pattern))
        
        python_files = [f for f in feature_files if f.suffix == '.py']
        
        if python_files:
            for py_file in python_files:
                generator.generate_test_file(py_file, output_dir)
        else:
            print(f"⚠️  No Python files found for feature: {args.feature}")
    
    else:
        # Generate tests for all components
        # Backend tests
        backend_dir = Path("backend")
        if backend_dir.exists():
            print("📁 Generating backend tests...")
            generator.generate_tests_for_directory(backend_dir, output_dir / "backend")
        
        # Frontend JavaScript tests (basic templates)
        frontend_dir = Path("frontend")
        if frontend_dir.exists():
            print("📁 Frontend tests would require JavaScript test generation")
            print("💡 Consider using Jest or similar for JavaScript testing")
    
    print("✅ Test generation complete!")
    print(f"📝 Review generated tests in {output_dir}")
    print("💡 Remember to:")
    print("   - Add appropriate test data")
    print("   - Customize assertions based on expected behavior")
    print("   - Mock external dependencies")
    print("   - Run tests to ensure they pass")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())