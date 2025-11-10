# Contributing to AI Agents Course

Thank you for your interest in contributing to this project! This guide will help you get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-agents-course.git
   cd ai-agents-course
   ```

3. **Set up your environment**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   export GOOGLE_GENAI_USE_VERTEXAI="FALSE"
   ```

## Development Workflow

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test them:
   ```bash
   # For Flask app
   cd web-chat
   python3 server.py

   # For Gradio app
   python3 gradio_app.py
   ```

3. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub

## Code Style

- Follow PEP 8 for Python code
- Use clear, descriptive variable names
- Add comments for complex logic
- Keep functions focused and modular

## Areas for Contribution

- **New Features**: Additional tools, agent capabilities
- **UI Improvements**: Enhanced styling, new themes
- **Documentation**: Tutorials, examples, guides
- **Bug Fixes**: Report and fix issues
- **Testing**: Add test coverage

## Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages or logs

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
