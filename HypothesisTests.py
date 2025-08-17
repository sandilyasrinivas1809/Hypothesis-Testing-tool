"""
Statistical Hypothesis Testing Library

This module provides a comprehensive framework for performing various statistical hypothesis tests
including one-sample, two-sample, and multiple-sample tests.

Author: Assistant
Version: 2.0
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats import weightstats as stests
from scipy.stats import (
    ttest_1samp, ttest_ind, ttest_rel, f_oneway, median_test,
    kruskal, wilcoxon, mannwhitneyu
)
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any, Optional, Tuple
from enum import Enum
import warnings
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TailType(Enum):
    """Enumeration for tail types in hypothesis testing."""
    TWO_TAIL = 'twoTail'
    ONE_TAIL_GREATER = 'oneTailG'
    ONE_TAIL_LESS = 'oneTailL'

@dataclass
class TestResult:
    """
    Data class to store hypothesis test results.
    """
    statistic: float
    pvalue: float
    alpha: float
    test_name: str
    null_hypothesis_accepted: bool
    
    @property
    def is_significant(self) -> bool:
        """Returns True if the result is statistically significant."""
        return self.pvalue <= self.alpha
    
    def __str__(self) -> str:
        return (f"{self.test_name}: statistic={self.statistic:.4f}, "
                f"p-value={self.pvalue:.4f}, alpha={self.alpha}, "
                f"result={'Accept H0' if self.null_hypothesis_accepted else 'Reject H0'}")

def validate_alpha(alpha: float) -> None:
    """Validates alpha value."""
    if not 0 < alpha < 1:
        raise ValueError(f"Alpha must be between 0 and 1, got {alpha}")

def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Validates DataFrame and required columns."""
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

def check_column_numeric(df: pd.DataFrame, column: str) -> None:
    """Checks if column contains numeric data."""
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must contain numeric data")

def print_test_results(result: TestResult) -> bool:
    """
    Prints the test results in a formatted way.
    
    Args:
        result: TestResult object containing test information
        
    Returns:
        bool: True if null hypothesis is accepted, False otherwise
    """
    print(f"\n{result.test_name} Results:")
    print(f"Test Statistic: {result.statistic:.4f}")
    print(f"P-value: {result.pvalue:.4f}")
    print(f"Alpha: {result.alpha}")
    print(f"Decision: {'Accept H0' if result.null_hypothesis_accepted else 'Reject H0'}")
    print("-" * 50)
    
    return result.null_hypothesis_accepted

class HypothesisTest(ABC):
    """
    Abstract Base Class for all hypothesis tests.
    Defines the common interface for running a hypothesis test.
    """
    
    def __init__(self, tails: Optional[TailType] = None):
        self.tails = tails
        self.test_name = self.__class__.__name__
    
    @abstractmethod
    def run_test(self, *args: Any, **kwargs: Any) -> bool:
        """
        Runs the specific hypothesis test.
        
        Returns:
            bool: True if null hypothesis is accepted, False otherwise
        """
        pass
    
    def _create_result(self, statistic: float, pvalue: float, alpha: float) -> TestResult:
        """Creates a TestResult object."""
        null_accepted = pvalue >= alpha
        return TestResult(
            statistic=statistic,
            pvalue=pvalue,
            alpha=alpha,
            test_name=self.test_name,
            null_hypothesis_accepted=null_accepted
        )

class OneSampleTTest(HypothesisTest):
    """Performs a one-sample t-test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "One-Sample T-Test"
    
    def run_test(self, column: List[str], alpha: float, data: pd.DataFrame, 
                 target_value: float) -> bool:
        """
        Runs the one-sample t-test.
        
        Args:
            column: List containing the column name
            alpha: Significance level
            data: DataFrame containing the data
            target_value: Hypothesized population mean
            
        Returns:
            bool: True if null hypothesis is accepted, False otherwise
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column)
            check_column_numeric(data, column[0])
            
            col_data = data[column[0]].dropna()
            
            if len(col_data) < 2:
                raise ValueError("Insufficient data points for t-test")
            
            # Perform the appropriate t-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = ttest_1samp(col_data, popmean=target_value)
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = ttest_1samp(col_data, popmean=target_value, alternative="greater")
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = ttest_1samp(col_data, popmean=target_value, alternative="less")
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in one-sample t-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class OneSampleZTest(HypothesisTest):
    """Performs a one-sample z-test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "One-Sample Z-Test"
    
    def run_test(self, column: List[str], alpha: float, data: pd.DataFrame, 
                 target_value: float) -> bool:
        """
        Runs the one-sample z-test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column)
            check_column_numeric(data, column[0])
            
            col_data = data[column[0]].dropna()
            
            if len(col_data) < 30:
                warnings.warn("Sample size < 30. Consider using t-test instead.")
            
            # Perform the appropriate z-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = stests.ztest(col_data, x2=None, value=target_value)
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = stests.ztest(col_data, x2=None, value=target_value, alternative="larger")
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = stests.ztest(col_data, x2=None, value=target_value, alternative="smaller")
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in one-sample z-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class TwoSampleTTest(HypothesisTest):
    """Performs a two-sample t-test (Student's t-test)."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Two-Sample T-Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the two-sample t-test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) < 2 or len(group2) < 2:
                raise ValueError("Insufficient data in one or both groups")
            
            # Perform the appropriate t-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=True)
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=True, alternative='greater')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=True, alternative='less')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in two-sample t-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class TwoSampleZTest(HypothesisTest):
    """Performs a two-sample z-test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Two-Sample Z-Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the two-sample z-test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) < 30 or len(group2) < 30:
                warnings.warn("Sample sizes < 30. Consider using t-test instead.")
            
            # Perform the appropriate z-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = stests.ztest(group1, group2, value=0, alternative='two-sided')
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = stests.ztest(group1, group2, value=0, alternative='larger')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = stests.ztest(group1, group2, value=0, alternative='smaller')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in two-sample z-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class WelchTTest(HypothesisTest):
    """Performs Welch's t-test (unequal variances)."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Welch's T-Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs Welch's t-test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) < 2 or len(group2) < 2:
                raise ValueError("Insufficient data in one or both groups")
            
            # Perform the appropriate t-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=False)
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=False, alternative='greater')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = ttest_ind(group1, group2, equal_var=False, alternative='less')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in Welch's t-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class PairedTTest(HypothesisTest):
    """Performs a paired t-test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Paired T-Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the paired t-test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) != len(group2):
                raise ValueError("Groups must have equal sample sizes for paired t-test")
            
            # Perform the appropriate paired t-test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = ttest_rel(group1, group2, alternative='two-sided')
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = ttest_rel(group1, group2, alternative='greater')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = ttest_rel(group1, group2, alternative='less')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in paired t-test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class WilcoxonTest(HypothesisTest):
    """Performs the Wilcoxon signed-rank test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Wilcoxon Signed-Rank Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the Wilcoxon signed-rank test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) != len(group2):
                raise ValueError("Groups must have equal sample sizes for Wilcoxon test")
            
            # Perform the appropriate Wilcoxon test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = wilcoxon(group1, group2, alternative='two-sided', mode='auto')
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = wilcoxon(group1, group2, alternative='greater', mode='auto')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = wilcoxon(group1, group2, alternative='less', mode='auto')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in Wilcoxon test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class MannWhitneyUTest(HypothesisTest):
    """Performs the Mann-Whitney U test."""
    
    def __init__(self, tails: Optional[TailType] = None):
        super().__init__(tails)
        self.test_name = "Mann-Whitney U Test"
    
    def run_test(self, column: List[str], cat: str, col1: str, col2: str, 
                 alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the Mann-Whitney U test.
        """
        try:
            validate_alpha(alpha)
            validate_dataframe(data, column + [cat])
            check_column_numeric(data, column[0])
            
            group1 = data[data[cat] == col1][column[0]].dropna()
            group2 = data[data[cat] == col2][column[0]].dropna()
            
            if len(group1) < 3 or len(group2) < 3:
                raise ValueError("Each group must have at least 3 observations")
            
            # Perform the appropriate Mann-Whitney U test based on tail type
            if self.tails == TailType.TWO_TAIL:
                statistic, pvalue = mannwhitneyu(group1, group2, alternative='two-sided')
            elif self.tails == TailType.ONE_TAIL_GREATER:
                statistic, pvalue = mannwhitneyu(group1, group2, alternative='greater')
            elif self.tails == TailType.ONE_TAIL_LESS:
                statistic, pvalue = mannwhitneyu(group1, group2, alternative='less')
            else:
                raise ValueError(f"Invalid tail type: {self.tails}")
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in Mann-Whitney U test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class ANOVA(HypothesisTest):
    """Performs one-way ANOVA."""
    
    def __init__(self):
        super().__init__(None)
        self.test_name = "One-Way ANOVA"
    
    def run_test(self, column: List[str], s1: pd.DataFrame, s2: pd.DataFrame, 
                 s3: pd.DataFrame, alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs one-way ANOVA.
        """
        try:
            validate_alpha(alpha)
            col_name = column[0]
            
            group1 = s1[col_name].dropna()
            group2 = s2[col_name].dropna()
            group3 = s3[col_name].dropna()
            
            if len(group1) < 2 or len(group2) < 2 or len(group3) < 2:
                raise ValueError("Each group must have at least 2 observations")
            
            statistic, pvalue = f_oneway(group1, group2, group3)
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in ANOVA: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class KruskalWallisTest(HypothesisTest):
    """Performs Kruskal-Wallis H test."""
    
    def __init__(self):
        super().__init__(None)
        self.test_name = "Kruskal-Wallis H Test"
    
    def run_test(self, column: List[str], s1: pd.DataFrame, s2: pd.DataFrame, 
                 s3: pd.DataFrame, alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs the Kruskal-Wallis H test.
        """
        try:
            validate_alpha(alpha)
            col_name = column[0]
            
            group1 = s1[col_name].dropna()
            group2 = s2[col_name].dropna()
            group3 = s3[col_name].dropna()
            
            if len(group1) < 5 or len(group2) < 5 or len(group3) < 5:
                warnings.warn("Groups should have at least 5 observations each for reliable results")
            
            statistic, pvalue = kruskal(group1, group2, group3)
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in Kruskal-Wallis test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class MoodsMedianTest(HypothesisTest):
    """Performs Mood's median test."""
    
    def __init__(self):
        super().__init__(None)
        self.test_name = "Mood's Median Test"
    
    def run_test(self, column: List[str], s1: pd.DataFrame, s2: pd.DataFrame, 
                 s3: pd.DataFrame, alpha: float, data: pd.DataFrame) -> bool:
        """
        Runs Mood's median test.
        """
        try:
            validate_alpha(alpha)
            col_name = column[0]
            
            group1 = s1[col_name].dropna()
            group2 = s2[col_name].dropna()
            group3 = s3[col_name].dropna()
            
            if len(group1) < 2 or len(group2) < 2 or len(group3) < 2:
                raise ValueError("Each group must have at least 2 observations")
            
            statistic, pvalue, _, _ = median_test(group1, group2, group3)
            
            result = self._create_result(statistic, pvalue, alpha)
            return print_test_results(result)
            
        except Exception as e:
            logger.error(f"Error in Mood's median test: {str(e)}")
            print(f"Error: {str(e)}")
            return False

class HypothesisTestInterface:
    """
    Interface for managing and selecting hypothesis tests.
    """
    
    def __init__(self):
        self.test_registry: Dict[str, Dict[str, type]] = {
            "oneSample": {
                't': OneSampleTTest,
                'z': OneSampleZTest,
            },
            'twoSample': {
                't': TwoSampleTTest,
                'z': TwoSampleZTest,
                'welcht': WelchTTest,
                'pairedt': PairedTTest,
                'wilcoxon': WilcoxonTest,
                'mannwitney': MannWhitneyUTest,
            },
            'morethantwoSample': {
                'anova': ANOVA,
                'kruskal': KruskalWallisTest,
                'moods': MoodsMedianTest,
            }
        }
    
    def select_test(self, samples: str, test: str, tails: TailType) -> HypothesisTest:
        """
        Selects and instantiates a hypothesis test.
        
        Args:
            samples: Type of sample test
            test: Specific test type
            tails: Tail type for the test
            
        Returns:
            HypothesisTest: Instantiated test object
        """
        try:
            test_class = self.test_registry[samples][test]
            return test_class(tails)
        except KeyError as e:
            raise ValueError(f"Unknown test configuration: {samples}/{test}") from e
    
    def select_test_more_than_two_samples(self, samples: str, test: str) -> HypothesisTest:
        """
        Selects and instantiates a multiple-sample hypothesis test.
        
        Args:
            samples: Type of sample test  
            test: Specific test type
            
        Returns:
            HypothesisTest: Instantiated test object
        """
        try:
            test_class = self.test_registry[samples][test]
            return test_class()
        except KeyError as e:
            raise ValueError(f"Unknown test configuration: {samples}/{test}") from e
    
    def get_available_tests(self) -> Dict[str, List[str]]:
        """Returns available tests by category."""
        return {category: list(tests.keys()) for category, tests in self.test_registry.items()}

def main(csv_file_path: str = "cereal.csv") -> None:
    """
    Main function for command-line usage.
    
    Args:
        csv_file_path: Path to the CSV file
    """
    try:
        htI = HypothesisTestInterface()
        
        print("Available test categories:")
        for category, tests in htI.get_available_tests().items():
            print(f"  {category}: {', '.join(tests)}")
        
        # Example usage would go here
        print(f"\nTo use this library, load your data from {csv_file_path} and select appropriate tests.")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()