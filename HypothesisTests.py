import pandas as pd
import scipy.stats as stats
from statsmodels.stats import weightstats as stests
from scipy.stats import ttest_1samp
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
from scipy.stats import median_test
from abc import ABC, abstractmethod
 
# class hypothesisTest(ABC):
 
#     @abstractmethod
#     def run_test(self):
#         pass

class HypothesisTestInterface():
    def __init__(self):
        self.test_set ={
            "oneSample":{
                't':oneSamplet,
                'z':oneSamplez,
            },
            'twoSample':{
                't':twoSamplet,
                'z':twoSamplez,
                'welcht':welcht,
                'pairedt':pairedt,
                'wilcoxon':wilcoxon,
                'mannwitney': mannwhitneyu,
            },
            'morethantwoSample':{
                'anova':anova,
                'kruskal': kruskaltest,
                'moods' : moodsmediantest,
            }
        }
        pass

    def select_test(self,samples,test,tails,type=None):
        return self.test_set[samples][test](tails)

    def select_test1(self,samples1,test1,type=None):
        return self.test_set[samples1][test1]

class oneSamplet():
    def __init__(self,tails=None):
        self.tails = tails
    
    def run_test(self, column, alpha, data, target_value):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic, pval = ttest_1samp(df[self.inp], popmean=target_value)
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False 
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic, pval = ttest_1samp(df[self.inp], popmean=target_value,alternative="greater")
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if pval < abs(alpha):
                return False
            else:
                return True
            
        elif self.tails == 'oneTailL':
            statistic, pval = ttest_1samp(df[self.inp], popmean=target_value,alternative="less")
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if pval < abs(alpha):
                return False
            else:
                return True
        
        
class oneSamplez():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, alpha, data, target_value):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic,pval = stests.ztest(df[self.inp], x2=None, value=target_value)
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic,pval = stests.ztest(df[self.inp], x2=None, value=target_value,alternative="larger")
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if pval < abs(alpha):
                return False
            else:
                return True
            
        elif self.tails == 'oneTailL':
            statistic,pval = stests.ztest(df[self.inp], x2=None, value=target_value,alternative="smaller")
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if pval < abs(alpha):
                return False
            else:
                return True

class twoSamplet():
    def __init__(self,tails=None):
        self.tails = tails

    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=True)
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=True,alternative='greater')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=True,alternative='less')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True

class twoSamplez():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic ,pval = stests.ztest(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],value=0,alternative='two-sided')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic ,pval = stests.ztest(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],value=0,alternative='larger')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic ,pval = stests.ztest(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],value=0,alternative='smaller')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        

class welcht():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=False)
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=False,alternative='greater')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic,pval=ttest_ind(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  equal_var=False,alternative='less')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
class pairedt():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic,pval=stats.ttest_rel(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2], alternative='two-sided')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic,pval=stats.ttest_rel(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2], alternative='greater')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic,pval=stats.ttest_rel(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2], alternative='less')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True

class wilcoxon():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic, pval = stats.wilcoxon(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  alternative='two-sided', mode='auto') 
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic, pval = stats.wilcoxon(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2], alternative='greater', mode='auto') 
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic, pval = stats.wilcoxon(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],  alternative='less', mode='auto') 
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True

class mannwhitneyu():
    def __init__(self,tails=None):
        self.tails = tails
    def run_test(self, column, cat, col1, col2,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        self.inp = column[0]   
        if self.tails == 'twoTail':
            statistic,pval= stats.mannwhitneyu(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],alternative='two-sided')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailG':
            statistic,pval= stats.mannwhitneyu(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],alternative='greater')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True
        elif self.tails == 'oneTailL':
            statistic,pval= stats.mannwhitneyu(df[self.inp][df[cat] == col1 ], df[self.inp][df[cat]== col2],alternative='less')
            print("\nThe Statistic value is:",round(statistic,2),"\n")
            print("The Pvalue is:",round(pval,2) ,"\n")
            if  pval < abs(alpha):
                return False
            else:
                return True

class anova(): 
    def run_test1(column,s1,s2,s3,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        inp = column[0]   
        statistic, pval = f_oneway(s1[inp],s2[inp],s3[inp])
        print("\nThe Statistic value is:",round(statistic,2),"\n")
        print("The Pvalue is:",round(pval,2) ,"\n")
        if pval<alpha:
           return False
        else:
            return True

class kruskaltest():
    
    def run_test1(column,s1,s2,s3,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        inp = column[0]   
        statistic,pval=stats.kruskal(s1[inp],s2[inp],s3[inp])
        print("\nThe Statistic value is:",round(statistic,2),"\n")
        print("The Pvalue is:",round(pval,2) ,"\n")
        if pval<alpha:
           return False
        else:
            return True

class moodsmediantest():
    def run_test1(column,s1,s2,s3,alpha, data):
        df = data
        columns = df.columns.tolist()
        if column[0] not in columns:
            return
        inp = column[0]   
        statistic,pval,m, table = median_test(s1[inp],s2[inp],s3[inp])
        print("\nThe Statistic value is:",round(statistic,2),"\n")
        print("The Pvalue is:",round(pval,2) ,"\n")
        if pval<alpha:
           return False
        else:
            return True

if __name__ =='__main__':
    htI = HypothesisTestInterface()
    sample_test= input("""Enter which Hypothesis test you want to perform
                    1. One sample Tests(oneSample)
                    2. Two Sample Tests(twoSample)
                    3. More than two sample Tests(morethantwoSample)
                    \n""")
    if sample_test == "oneSample":    
        inp_test = input("""Enter which test 
                        1.One sample t test(t)
                        2.One sample z test(z)\n""")
        tail_sel = input("""Enter which type of tailed test you want to perform:
                        1. Two Tailed Test(twoTail)
                        2. One Tailed Test upper(oneTailG)
                        3. One Tailed Test lower(oneTailL)\n""")
        myTest = htI.select_test(samples=sample_test,test = inp_test, tails=tail_sel,type=None)
        df = pd.read_csv("cereal.csv")
        print(df.columns)
        col = input("write column name \n")
        print("The sample mean of" ,col,"is:")
        print(round(df[col].mean(),2))
        target_val = input("Please enter population mean value \n")
        alpha_val = float(input("Please enter the Alpha value \n"))
        if myTest.run_test([col], alpha_val,df, float(target_val)):
            print("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
        else:
            print("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")

    elif sample_test == "twoSample":
        inp_test = input("""Enter which you want to perform:
                        1.Two sample t test(t)
                        2.Two sample z test(z)
                        3. Welch t test(welcht)
                        5. Paired t test(pairedt)
                        4. Wilcoxon signed rank(wilcoxon)
                        5. Mann Witney U test(mannwitney)\n""")
        tail_sel = input("""Enter which type of tailed test you want to perform:
                        1. Two Tailed Test(twoTail)
                        2. One Tailed Test upper(oneTailG)
                        3. One Tailed Test lower(oneTailL)\n""")
        myTest = htI.select_test(samples=sample_test,test = inp_test, tails=tail_sel,type=None)
        df = pd.read_csv("cereal.csv")
        print(df.columns)
        col = input("write column name \n")
        alpha_val = float(input("Please enter the Alpha value \n"))
        category = input("Enter the column you want to compare with \n")
        print(df[category].unique())
        column1 = input("Enter category 1 here: ")
        column2 = input("Enter category 2 here: ")
        if myTest.run_test([col],category,column1,column2,alpha_val,df):
            print("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
        else:
            print("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
    
    else:
        inp_test = input("""Enter which you want to perform:
                        1.Analysis of Variance(anova)
                        2.Kruskal Wallis H test(kruskal)
                        3. Moods Median Test(moods)\n""")
        myTest1 = htI.select_test1(samples1=sample_test, test1=inp_test,type=None)
        df = pd.read_csv(r"C:\Users\sandilya_garimella\Documents\Sandilya\Hypothesis Testing\Final\cereal.csv")
        print(df.columns)
        col = input("write column name \n")
        alpha_val = float(input("Please enter the Alpha value \n"))
        category = input("Enter the column you want to compare with \n")
        print(df[category].unique())
        column1 = input("Enter category 1 here: ")
        column2 = input("Enter category 2 here: ")
        column3 = input("Enter category 3 here. ")
        category1 = df[df[category] == column1]
        category2 = df[df[category] == column2]
        category3 = df[df[category] == column3]
        if myTest1.run_test1([col],category1,category2,category3,alpha_val,df):            
            print("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
        else:
            print("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")