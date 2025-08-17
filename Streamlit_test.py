import streamlit as st
import pandas as pd
import numpy as np
from HypothesisTests import HypothesisTestInterface, TailType
from typing import List, Union, Dict, Any, Optional, Tuple
import time

# Configure page settings
st.set_page_config(
    page_title="Hypothesis Testing Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Statistical Hypothesis Testing Tool")
st.markdown("Upload your data and perform various statistical hypothesis tests with ease.")

# Initialize session state
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None

@st.cache_data
def load_data(uploaded_file: Any) -> Optional[pd.DataFrame]:
    """
    Loads and validates data from an uploaded file.
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if df.empty:
                st.error("The uploaded file is empty.")
                return None
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    return None

@st.cache_data
def get_numerical_columns(df: pd.DataFrame) -> List[str]:
    """
    Returns list of numerical columns from the DataFrame.
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()

@st.cache_data
def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """
    Returns list of categorical columns from the DataFrame.
    """
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def display_test_results(test_accepted: bool, statistic: float = None, pval: float = None) -> None:
    """
    Displays the outcome of the hypothesis test with better formatting.
    """
    if statistic is not None and pval is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Test Statistic", f"{statistic:.4f}")
        with col2:
            st.metric("P-value", f"{pval:.4f}")
    
    if test_accepted:
        st.success("✅ **ACCEPT** the null hypothesis (p-value > α)")
    else:
        st.error("❌ **REJECT** the null hypothesis (p-value ≤ α)")

def validate_inputs(alpha: float) -> bool:
    """
    Validates user inputs.
    """
    if alpha <= 0 or alpha >= 1:
        st.error("Alpha value must be between 0 and 1.")
        return False
    return True

def get_column_selection(df: pd.DataFrame, label: str, key: str) -> Optional[str]:
    """
    Gets column selection from user and validates if it's numerical.
    """
    numerical_cols = get_numerical_columns(df)
    if not numerical_cols:
        st.error("No numerical columns found in the dataset.")
        return None
    
    cols = st.selectbox(
        label, 
        options=["Select a column..."] + numerical_cols,
        key=key,
        help="Choose a numerical column for analysis"
    )
    
    if cols == "Select a column...":
        return None
    return cols

def get_category_column_selection(df: pd.DataFrame, key: str) -> Optional[str]:
    """
    Gets categorical column selection for grouping.
    """
    categorical_cols = get_categorical_columns(df)
    if not categorical_cols:
        st.error("No categorical columns found for grouping.")
        return None
    
    return st.selectbox(
        "Select grouping column:",
        options=["Select a column..."] + categorical_cols,
        key=key,
        help="Choose a categorical column for grouping"
    )

def get_categories_selection(df: pd.DataFrame, category_col: str, num_categories: int, key: str) -> Optional[List[str]]:
    """
    Gets category selections from user with validation.
    """
    unique_categories = df[category_col].unique().tolist()
    
    if len(unique_categories) < num_categories:
        st.error(f"The selected column has only {len(unique_categories)} unique values. Need at least {num_categories}.")
        return None
    
    selected_categories = st.multiselect(
        f'Select exactly {num_categories} categories:', 
        options=unique_categories,
        key=key,
        help=f"Choose exactly {num_categories} categories for comparison"
    )
    
    if len(selected_categories) != num_categories:
        if len(selected_categories) > 0:
            st.warning(f"Please select exactly {num_categories} categories. Currently selected: {len(selected_categories)}")
        return None
    return selected_categories

def create_data_summary(df: pd.DataFrame, column: str, category_col: str = None, categories: List[str] = None) -> None:
    """
    Creates a summary of the selected data.
    """
    st.subheader("📈 Data Summary")
    
    if category_col and categories:
        for i, cat in enumerate(categories):
            subset = df[df[category_col] == cat][column]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"{cat} - Count", len(subset))
            with col2:
                st.metric(f"{cat} - Mean", f"{subset.mean():.4f}")
            with col3:
                st.metric(f"{cat} - Std", f"{subset.std():.4f}")
            with col4:
                st.metric(f"{cat} - Median", f"{subset.median():.4f}")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Count", len(df[column]))
        with col2:
            st.metric("Mean", f"{df[column].mean():.4f}")
        with col3:
            st.metric("Std", f"{df[column].std():.4f}")
        with col4:
            st.metric("Median", f"{df[column].median():.4f}")

def run_one_sample_tests(df: pd.DataFrame, htI: HypothesisTestInterface) -> None:
    """
    Interface for one-sample tests.
    """
    st.subheader("🔍 One Sample Tests")
    
    test_options = {
        "One sample t-test (Two-tailed)": ("t", TailType.TWO_TAIL),
        "One sample z-test (Two-tailed)": ("z", TailType.TWO_TAIL),
        "One sample t-test (Lower-tailed)": ("t", TailType.ONE_TAIL_LESS),
        "One sample z-test (Lower-tailed)": ("z", TailType.ONE_TAIL_LESS),
        "One sample t-test (Upper-tailed)": ("t", TailType.ONE_TAIL_GREATER),
        "One sample z-test (Upper-tailed)": ("z", TailType.ONE_TAIL_GREATER),
    }
    
    test_inp = st.selectbox("Select test type:", list(test_options.keys()), key="one_sample_test")
    
    cols = get_column_selection(df, 'Select the column for analysis:', 'one_sample_column')
    if cols:
        create_data_summary(df, cols)
        
        col1, col2 = st.columns(2)
        with col1:
            target_value = st.number_input(
                "Population mean (μ₀):", 
                value=0.0, 
                help="Enter the hypothesized population mean"
            )
        with col2:
            alpha = st.number_input(
                "Significance level (α):", 
                value=0.05, 
                min_value=0.001, 
                max_value=0.999, 
                step=0.001,
                help="Enter the significance level (typically 0.05)"
            )
        
        if validate_inputs(alpha) and st.button("🚀 Run Test", type="primary"):
            test_type_str, tail_type_enum = test_options[test_inp]
            myTest = htI.select_test(samples="oneSample", test=test_type_str, tails=tail_type_enum)
            
            with st.spinner("Running hypothesis test..."):
                time.sleep(0.5)  # Brief delay for UX
                result = myTest.run_test([cols], alpha, df, target_value)
                display_test_results(result)

def run_two_sample_tests(df: pd.DataFrame, htI: HypothesisTestInterface) -> None:
    """
    Interface for two-sample tests.
    """
    st.subheader("🔍 Two Sample Tests")
    
    test_options = {
        "Two sample t-test (Two-tailed)": ("t", TailType.TWO_TAIL),
        "Two sample z-test (Two-tailed)": ("z", TailType.TWO_TAIL),
        "Two sample t-test (Lower-tailed)": ("t", TailType.ONE_TAIL_LESS),
        "Two sample z-test (Lower-tailed)": ("z", TailType.ONE_TAIL_LESS),
        "Two sample t-test (Upper-tailed)": ("t", TailType.ONE_TAIL_GREATER),
        "Two sample z-test (Upper-tailed)": ("z", TailType.ONE_TAIL_GREATER),
        "Welch's t-test (Two-tailed)": ("welcht", TailType.TWO_TAIL),
        "Welch's t-test (Lower-tailed)": ("welcht", TailType.ONE_TAIL_LESS),
        "Welch's t-test (Upper-tailed)": ("welcht", TailType.ONE_TAIL_GREATER),
        "Wilcoxon signed-rank (Two-tailed)": ("wilcoxon", TailType.TWO_TAIL),
        "Wilcoxon signed-rank (Lower-tailed)": ("wilcoxon", TailType.ONE_TAIL_LESS),
        "Wilcoxon signed-rank (Upper-tailed)": ("wilcoxon", TailType.ONE_TAIL_GREATER),
        "Mann-Whitney U (Two-tailed)": ("mannwitney", TailType.TWO_TAIL),
        "Mann-Whitney U (Lower-tailed)": ("mannwitney", TailType.ONE_TAIL_LESS),
        "Mann-Whitney U (Upper-tailed)": ("mannwitney", TailType.ONE_TAIL_GREATER)
    }
    
    test_inp = st.selectbox("Select test type:", list(test_options.keys()), key="two_sample_test")
    
    cols = get_column_selection(df, 'Select the column for analysis:', 'two_sample_column')
    if cols:
        category = get_category_column_selection(df, 'two_sample_category')
        if category and category != "Select a column...":
            selected_columns = get_categories_selection(df, category, 2, 'two_sample_categories')
            if selected_columns:
                create_data_summary(df, cols, category, selected_columns)
                
                alpha = st.number_input(
                    "Significance level (α):", 
                    value=0.05, 
                    min_value=0.001, 
                    max_value=0.999, 
                    step=0.001,
                    key="two_sample_alpha"
                )
                
                if validate_inputs(alpha) and st.button("🚀 Run Test", type="primary", key="run_two_sample"):
                    test_type_str, tail_type_enum = test_options[test_inp]
                    myTest = htI.select_test(samples="twoSample", test=test_type_str, tails=tail_type_enum)
                    
                    with st.spinner("Running hypothesis test..."):
                        time.sleep(0.5)
                        column1, column2 = selected_columns
                        result = myTest.run_test([cols], category, column1, column2, alpha, df)
                        display_test_results(result)

def run_multiple_sample_tests(df: pd.DataFrame, htI: HypothesisTestInterface) -> None:
    """
    Interface for multiple-sample tests.
    """
    st.subheader("🔍 Multiple Sample Tests")
    
    test_options = {
        "Analysis of Variance (ANOVA)": "anova",
        "Kruskal-Wallis H Test": "kruskal",
        "Mood's Median Test": "moods",
    }
    
    test_inp = st.selectbox("Select test type:", list(test_options.keys()), key="multi_sample_test")
    
    cols = get_column_selection(df, 'Select the column for analysis:', 'multi_sample_column')
    if cols:
        category = get_category_column_selection(df, 'multi_sample_category')
        if category and category != "Select a column...":
            selected_categories = get_categories_selection(df, category, 3, 'multi_sample_categories')
            if selected_categories:
                create_data_summary(df, cols, category, selected_categories)
                
                alpha = st.number_input(
                    "Significance level (α):", 
                    value=0.05, 
                    min_value=0.001, 
                    max_value=0.999, 
                    step=0.001,
                    key="multi_sample_alpha"
                )
                
                if validate_inputs(alpha) and st.button("🚀 Run Test", type="primary", key="run_multi_sample"):
                    test_type_str = test_options[test_inp]
                    myTest = htI.select_test_more_than_two_samples(samples="morethantwoSample", test=test_type_str)
                    
                    with st.spinner("Running hypothesis test..."):
                        time.sleep(0.5)
                        column1, column2, column3 = selected_categories
                        category1 = df[df[category] == column1]
                        category2 = df[df[category] == column2]
                        category3 = df[df[category] == column3]
                        result = myTest.run_test([cols], category1, category2, category3, alpha, df)
                        display_test_results(result)

# Main application logic
uploaded_file = st.file_uploader(
    "📁 Upload your CSV file", 
    type=['csv'], 
    help="Upload a CSV file containing your data"
)

df = load_data(uploaded_file)

if df is not None:
    # Display data info
    with st.expander("📊 Dataset Overview", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Numerical Columns", len(get_numerical_columns(df)))
        
        if st.checkbox("Show data preview"):
            st.dataframe(df.head(10), use_container_width=True)
    
    # Test selection
    selection = st.sidebar.selectbox(
        "🧪 Select Test Category:",
        ["Select test type...", "One sample tests", "Two sample tests", "Multiple sample tests"],
        help="Choose the type of hypothesis test to perform"
    )
    
    htI = HypothesisTestInterface()
    
    if selection == 'One sample tests':
        run_one_sample_tests(df, htI)
    elif selection == 'Two sample tests':
        run_two_sample_tests(df, htI)
    elif selection == "Multiple sample tests":
        run_multiple_sample_tests(df, htI)
    elif selection == "Select test type...":
        st.info("👆 Please select a test category from the sidebar to get started.")
else:
    st.info("👆 Please upload a CSV file to begin hypothesis testing.")
    
    # Show example
    with st.expander("💡 Example Usage"):
        st.markdown("""
        **Steps to perform hypothesis testing:**
        1. Upload a CSV file with your data
        2. Select the type of test from the sidebar
        3. Choose the appropriate columns for analysis
        4. Set your significance level (α)
        5. Run the test and interpret results
        
        **Supported test types:**
        - **One sample tests**: Compare sample mean to a known value
        - **Two sample tests**: Compare means between two groups
        - **Multiple sample tests**: Compare means across multiple groups
        """)