#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:25:36 2019

@author: Alexandr Moskalev (moskalev@umich.edu)

The MIT License (MIT)

Copyright (c) 2020 Alexandr Moskalev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
"""

# Default regression result wrapper
class regresult():
    
    def __init__(self, regression):
        self.regression = regression
        for attr in ['rsquared', 'rsquared_adj', 'fvalue', 'f_statistic']:
            if attr in dir(regression):
                self.setattr(self, attr, getattr(regression, attr))
        
    def __nobs(self):
        return self.regression.nobs
    
    def __params(self):
        return self.regression.params
    
    def __pvalues(self):
        return self.regression.pvalues
    
    def __index(self):
        return self.regression.index
    
    def __se(self):
        if 'bse' in dir(self.regression):
            se = self.regression.bse
        if 'std_errors' in dir(self.regression):
            se = self.regression.std_errors
        return se
    
    nobs = property(__nobs)
    params = property(__params)
    pvalues = property(__pvalues)
    index = property(__index)
    se = property(__se)


# Regression result wrapper for CoxTimeVarying from lifelines module
class regCoxTimeVarying(regresult):
    
    def __init__(self, regression):
        super(regCoxTimeVarying, self).__init__(regression)
        
    def __params(self):
        return self.regression.params_
    
    def __pvalues(self):
        return self.regression.summary['p']
    
    def __se(self):
        return self.regression.standard_errors_
    
    def __nobs(self):
        return self.regression.weights.sum()
    
    params = property(__params)
    pvalues = property(__pvalues)
    se = property(__se)
    nobs = property(__nobs)

    
class texression():
    
    def __init__(self, varnames={}, varorder=[], maxrows=100, head_legend="",
                 adjr2=False, include_std=True, new_str_ex=3,
                 intertable_fill="", longtable=False, ltcaption="", ltlabel="",
                 ltcolwidth=3, hide_r2fstat=False):
        self.results = []
        self.varnames = varnames
        self.varorder = varorder
        self.maxrows = maxrows
        self.head_legend = head_legend
        self.adjr2 = adjr2
        self.include_std = include_std
        self._new_str_ex = new_str_ex
        self.intertable_fill = intertable_fill
        self.longtable = longtable
        self.ltcaption = ltcaption
        self.ltlabel = ltlabel
        self.ltcolwidth = ltcolwidth
        self.hide_r2fstat = hide_r2fstat
        
    def add_regression(self, regression, depvar = ""):
        if regression.__class__.__name__ == 'CoxTimeVaryingFitter':
            regression = regCoxTimeVarying(regression)
        else:
            regression = regresult(regression)
        self.results.append({'r' : regression, 'depvar' : depvar})
        
    def __get_varname(self, v):
        if type(v) == dict:
            v = v['name']
        if v in self.varnames.keys():
            res = str(self.varnames[v])
        else:
            res = v.replace('_', '\_')
        return res
            
    def __gen_header(self, false_header = False):
        tot_cols = len(self.results) + 1 # To account for variable names
        
        if self.longtable: # Define the tabular/longtable environment
            res = "\LTcapwidth=\\textwidth\n\n" # mt command needs to be
                                                # defined somewhere else
            res += "\\begin{longtable}{l" + "D{.}{.}{5.6}" * (tot_cols - 1) \
            + "}\n"
            res += "\caption{" + self.ltcaption + "}\n"
            res += "\label{" + self.ltlabel + "} \\\ \n"
        else:
            res = "\\begin{tabular}{l" + "D{.}{.}{5}" * (tot_cols - 1) + "}\n"
        
        # Generate header
        if self.longtable:
            res += "\hline\hline\n"
            allvar = list(set([x['depvar'] for x in self.results]))
            if len(allvar) > 1: # We need to display these variables
                res += "\n"
                for i in range(1, tot_cols):
                    res += "& \mc{" + str(self.ltcolwidth) + "cm}{" \
                    + self.__get_varname(self.results[i - 1]['depvar']) \
                    + "}\n"
            res += "\\\ \n"
            for i in range(1, tot_cols):
                res += "& \multicolumn{1}{c}{{\it(" + str(i) + ")}}"
            res += "\\\ \hline\n\endfirsthead\n"
        else:
            if not false_header:
                res += "\hline\hline\n"
            if (not false_header)&(self.head_legend != ""):
                res += "\multicolumn{" + str(len(self.results) + 1) + "}{l}{" \
                + self.head_legend + "} \\\ \n"
            for i in range(1, tot_cols):
                res += "& \multicolumn{1}{c}{(" + str(i) + ")}"
            if false_header:
                res += "\\\ \hline \n"
            else:
                # Gather all the variables:
                allvar = list(set([x['depvar'] for x in self.results]))
                if len(allvar) > 1:
                    res += "\\\ \n"
                    for i in range(1, tot_cols):
                        res += "& \multicolumn{1}{c}{" \
                        + self.__get_varname(self.results[i - 1]['depvar']) \
                        + "}"
                res += "\\\ \hline \n"
            
        if self.longtable: # Since we have a longtable we need to generate
                           # secondary header and footer
            res += "\multicolumn{" + str(tot_cols) + "}{l}{Table \\ref{" \
            + self.ltlabel + "}, continued} \\\ \n"
            for i in range(1, tot_cols):
                res += "& \multicolumn{1}{c}{{\it(" + str(i) + ")}}"
            res += "\n\n\endhead\n\n\endfoot\n\n"
        return res
    
    def __get_false_footer(self):
        if self.longtable:
            res = "\hline\n\end{longtable}\n"
        else:
            res = "\hline\n\end{tabular}\n"
        res += self.intertable_fill + "\n"
        return res
        
    def __get_footer(self):
        res = "\hline\n"
        res += "Observations "
        for r in self.results:
            res += "& \multicolumn{1}{c}{" + "{0:.0f}".format(r['r'].nobs) \
            + "} "
        res += "\\\ \n"
        
        if self.hide_r2fstat == False:
            res += "$R^2$ "
            for r in self.results:
                if 'rsquared' in dir(r['r']):
                    res += "& \multicolumn{1}{c}{" \
                    + "{0:.3f}".format(r['r'].rsquared) + "} "
                else:
                    res += " & "
            res += "\\\ \n"
        
        if self.adjr2:
            res += "Adj. $R^2$ "
            for r in self.results:
                if 'rsquared_adj' in dir(r['r']):
                    res += "& \multicolumn{1}{c}{" \
                    + "{0:.3f}".format(r['r'].rsquared_adj) + "} "
                else:
                    res += " & "
            res += "\\\ \n"
        
        if self.hide_r2fstat == False:
            res += "F stat. "
            for r in self.results:
                res += " & "
                if 'fvalue' in dir(r['r']):
                    if r['r'].fvalue == r['r'].fvalue:
                        res += "\multicolumn{1}{c}{" \
                        + "{0:.1f}".format(r['r'].fvalue[0][0]) + "} "
                if 'f_statistic' in dir(r['r']):
                    res += "\multicolumn{1}{c}{" \
                    + "{0:.1f}".format(r['r'].f_statistic.stat) + "} "
                    
            res += "\\\ \n"
        
        res += "\hline\hline\n"
        res += "\multicolumn{" + str(len(self.results) + 1) \
        + "}{r}{$^*p < 0.1$; $^{**}p < 0.05$; $^{***}p < 0.01$}\n"
        if self.longtable:
            res += "\end{longtable}\n"
        else:
            res += "\end{tabular}\n"
        return res
    
    def __get_silent_vars(self):
        res = []
        for v in self.varorder:
            if type(v) == dict:
                if 'vars' in v.keys():
                    res += v['vars']
        return res
        
    def __get_varorder(self):
        all_vars = []
        for r in self.results:
            all_vars += list(r['r'].params.index)
        hashable_vars = [x for x in self.varorder if type(x) == str] # We need
                                        # to exclude any dicts from here first
        all_vars = list(set(all_vars) - set(hashable_vars)
                        - set(self.__get_silent_vars()) - set(['const']))
        if 'const' in self.varorder:
            return self.varorder + all_vars
        else:
            if 'const' in set(self.__get_silent_vars()):
                return self.varorder + all_vars
            else:
                return self.varorder + all_vars + ['const']
    
    def __get_table_string(self, v):
        res = "\\rule{0pt}{" + str(self._new_str_ex) + "ex} "
        
        if type(v) == dict: # For dict variables we need to use special rules
                        # as these may contain groups of regression variables
            if v['type'] == 'controls': # We are working with a group
                                        # of controls
                res += self.__get_varname(v)
                for r in self.results:
                    res += " & "
                    if set(v['vars']).issubset(set(r['r'].params.index)):
                        res += "\multicolumn{1}{c}{\\text{Yes}}"
                    else:
                        res += "\multicolumn{1}{c}{\\text{No}}"
                res += " \\\ \n"
                return res
            
            if v['type'] == 'silent': # Silence some variables as they make
                                      # no sense (like an empty constant)
                res = ""
                return res
            
            if v['type'] == 'separator':
                res = "\multicolumn{" + str(len(self.results) + 1) \
                + "}{l}{\\text{" + self.__get_varname(v) + "}}"
                res += " \\\* \n" # After a separator we do not want
                                  # to break the table in longtable
                return res
                
            return str(res + " <Error in texression>")
        
        res += self.__get_varname(v)        
        
        for r in self.results:
            res += " & "
            if v in r['r'].params.index:
                res += "{0:.3f}".format(r['r'].params[v]) + "^{"
                if r['r'].pvalues[v] <= 0.1:
                    res += "*"
                if r['r'].pvalues[v] <= 0.05:
                    res += "*"
                if r['r'].pvalues[v] <= 0.01:
                    res += "*"
                res += "}"
        
        if self.include_std: # Include standard errors
            res += " \\\* \n"
            for r in self.results:
                se = r['r'].se
                res += " & "
                if v in se.index:
                    res += "({0:.3f})".format(se[v])
        res += " \\\ \n"
        return res
        
    def __get_table_data(self):
        varorder = self.__get_varorder()
        res = ""
        row_cnt = 0
        for v in varorder:
            if row_cnt >= self.maxrows:
                res += self.__get_false_footer() \
                + self.__gen_header(false_header = True)
                row_cnt = 0
            res += self.__get_table_string(v)
            row_cnt += 1
        return res
        
    def latex(self, file=""):
        res = self.__gen_header() + self.__get_table_data() \
        + self.__get_footer()
        if file != "":
            with open(file, 'w') as f:
                f.write(res)
        else:
            return res
