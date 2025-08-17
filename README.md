# 📊 Statistical Hypothesis Testing Tool

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.25+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)

*A comprehensive statistical hypothesis testing library with an intuitive web interface*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

The **Statistical Hypothesis Testing Tool** is a powerful Python library that provides a comprehensive suite of statistical tests with a beautiful, user-friendly Streamlit web interface. Whether you're a data scientist, researcher, or student, this tool makes statistical analysis accessible and intuitive.

### 🌟 Key Highlights

- **🔬 15+ Statistical Tests** - From basic t-tests to advanced non-parametric tests
- **🎨 Beautiful Web Interface** - Interactive Streamlit dashboard
- **📊 Real-time Visualization** - Data summaries and statistical metrics
- **✅ Input Validation** - Comprehensive error handling and warnings
- **📱 Responsive Design** - Works on desktop and mobile devices
- **🔧 Extensible Architecture** - Easy to add new tests and features

---

## 🚀 Features

### 📈 Supported Statistical Tests

| Category | Tests Available |
|----------|-----------------|
| **One Sample Tests** | • One-sample t-test<br>• One-sample z-test<br>• All with two-tailed and one-tailed variants |
| **Two Sample Tests** | • Independent t-test<br>• Welch's t-test<br>• Two-sample z-test<br>• Paired t-test<br>• Mann-Whitney U test<br>• Wilcoxon signed-rank test |
| **Multiple Sample Tests** | • One-way ANOVA<br>• Kruskal-Wallis H test<br>• Mood's median test |

### 🎨 User Interface Features

- **📊 Data Overview Dashboard** - Instant insights into your dataset
- **🔍 Smart Column Detection** - Automatic identification of numerical/categorical columns
- **📈 Statistical Summaries** - Mean, median, standard deviation, and count for each group
- **⚡ Real-time Validation** - Immediate feedback on data quality and test assumptions
- **🎯 Interactive Results** - Clear, formatted test results with statistical interpretation

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/hypothesis-testing-tool.git
cd hypothesis-testing-tool

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run Streamlit_test.py
```

### Dependencies

```
pandas>=1.5.0
scipy>=1.9.0
statsmodels>=0.13.0
numpy>=1.21.0
streamlit>=1.25.0
```

---

## 💻 Usage

### 🌐 Web Interface (Recommended)

1. **Launch the Application**
   ```bash
   streamlit run Streamlit_test.py
   ```

2. **Upload Your Data**
   - Supports CSV files
   - Automatic data validation
   - Preview your dataset

3. **Select Your Test**
   - Choose from one-sample, two-sample, or multiple-sample tests
   - Interactive test selection with descriptions

4. **Configure Parameters**
   - Select columns for analysis
   - Set significance level (α)
   - Choose test variants (one-tailed vs two-tailed)

5. **View Results**
   - Statistical test results
   - Clear interpretation
   - Export-ready format

### 🐍 Python Library

```python
from HypothesisTests import HypothesisTestInterface, TailType
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize the testing interface
test_interface = HypothesisTestInterface()

# Example: One-sample t-test
test = test_interface.select_test(
    samples="oneSample", 
    test="t", 
    tails=TailType.TWO_TAIL
)

result = test.run_test(
    column=['your_column'], 
    alpha=0.05, 
    data=data, 
    target_value=0
)

# Example: Two-sample t-test
test = test_interface.select_test(
    samples="twoSample", 
    test="t", 
    tails=TailType.TWO_TAIL
)

result = test.run_test(
    column=['measurement'], 
    cat='group', 
    col1='control', 
    col2='treatment',
    alpha=0.05, 
    data=data
)
```

---

## 📖 Documentation

### 🔬 Test Descriptions

#### One-Sample Tests
- **t-test**: Compare sample mean to a known population mean
- **z-test**: Similar to t-test but assumes known population variance

#### Two-Sample Tests
- **Independent t-test**: Compare means of two independent groups
- **Welch's t-test**: t-test without equal variance assumption
- **Paired t-test**: Compare paired observations
- **Mann-Whitney U**: Non-parametric alternative to independent t-test
- **Wilcoxon signed-rank**: Non-parametric alternative to paired t-test

#### Multiple-Sample Tests
- **ANOVA**: Compare means across multiple groups
- **Kruskal-Wallis**: Non-parametric alternative to ANOVA
- **Mood's Median**: Compare medians across groups

### 🎯 API Reference

#### `HypothesisTestInterface`

Main interface for selecting and running tests.

**Methods:**
- `select_test(samples, test, tails)` - Select one/two-sample tests
- `select_test_more_than_two_samples(samples, test)` - Select multiple-sample tests
- `get_available_tests()` - List all available tests

#### `TailType` Enum

- `TWO_TAIL` - Two-tailed test
- `ONE_TAIL_GREATER` - Upper-tailed test  
- `ONE_TAIL_LESS` - Lower-tailed test

---

## 📁 Project Structure

```
hypothesis-testing-tool/
│
├── 📄 HypothesisTests.py      # Core statistical testing library
├── 🎨 Streamlit_test.py       # Streamlit web interface
├── 📋 requirements.txt        # Python dependencies
├── 🙈 .gitignore             # Git ignore rules
├── 📖 README.md              # Project documentation
│
└── 📊 sample_data/            # Example datasets (not tracked)
    ├── cereal.csv
    └── examples.csv
```

---

## 🔧 Advanced Features

### 🛡️ Input Validation

- **Data Type Checking**: Ensures numerical columns for statistical tests
- **Sample Size Validation**: Warns about insufficient data
- **Missing Value Handling**: Automatic removal with notifications
- **Statistical Assumptions**: Warnings for violated assumptions

### 📊 Enhanced Results

```python
# TestResult object with rich information
@dataclass
class TestResult:
    statistic: float
    pvalue: float
    alpha: float
    test_name: str
    null_hypothesis_accepted: bool
    
    @property
    def is_significant(self) -> bool:
        return self.pvalue <= self.alpha
```

### 🎨 Customization

The tool is designed to be easily extensible:

```python
# Add custom tests by inheriting from HypothesisTest
class CustomTest(HypothesisTest):
    def run_test(self, *args, **kwargs):
        # Your custom implementation
        pass
```

---

## 🎯 Examples

### Example 1: Quality Control Analysis

```python
# Test if product measurements meet specification
test = interface.select_test("oneSample", "t", TailType.TWO_TAIL)
result = test.run_test(['measurement'], 0.05, data, target_specification)
```

### Example 2: A/B Testing

```python
# Compare conversion rates between two variants
test = interface.select_test("twoSample", "t", TailType.TWO_TAIL)
result = test.run_test(['conversion_rate'], 'variant', 'A', 'B', 0.05, data)
```

### Example 3: Multi-group Comparison

```python
# Compare performance across multiple treatments
test = interface.select_test_more_than_two_samples("morethantwoSample", "anova")
result = test.run_test(['performance'], group1_data, group2_data, group3_data, 0.05, data)
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🔧 Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/hypothesis-testing-tool.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### 📝 Contribution Guidelines

1. **🐛 Bug Reports**: Use GitHub issues with detailed descriptions
2. **✨ Feature Requests**: Propose new statistical tests or UI improvements
3. **📖 Documentation**: Help improve documentation and examples
4. **🧪 Testing**: Add tests for new features

### 🎯 Areas for Contribution

- [ ] Additional statistical tests (Bayesian, regression tests)
- [ ] Data visualization features
- [ ] Export functionality (PDF reports, Excel)
- [ ] Mobile optimization
- [ ] Multi-language support
- [ ] Performance optimizations

---

## 📊 Screenshots

### 🏠 Main Dashboard
*Beautiful, intuitive interface for data upload and test selection*

### 📈 Test Configuration
*Step-by-step guidance through test setup with real-time validation*

### 📋 Results Display
*Clear, professional results with statistical interpretation*

---

## 🏆 Why Choose This Tool?

| Feature | Our Tool | Alternatives |
|---------|----------|-------------|
| **Ease of Use** | ✅ Web interface + Python API | ❌ Command line only |
| **Validation** | ✅ Comprehensive input checking | ⚠️ Basic validation |
| **Documentation** | ✅ Extensive docs + examples | ⚠️ Minimal documentation |
| **Extensibility** | ✅ Easy to add new tests | ❌ Difficult to extend |
| **Modern UI** | ✅ Beautiful Streamlit interface | ❌ Outdated interfaces |
| **Error Handling** | ✅ Graceful error management | ⚠️ Cryptic error messages |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **SciPy** community for statistical computing foundations
- **Streamlit** team for the amazing web app framework
- **Pandas** developers for data manipulation capabilities
- **statsmodels** contributors for advanced statistical functions

---

## 📞 Support

- 📧 **Email**: sandilyasrinivasgarimella@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/sandilyasrinivas1809/hypothesis-testing-tool/issues)
- 📚 **Wiki**: [Project Wiki](https://github.com/sandilyasrinivas1809/hypothesis-testing-tool/wiki)

---

<div align="center">

**⭐ If you find this tool helpful, please consider giving it a star! ⭐**

Made with ❤️ by the Statistical Computing Community

</div>