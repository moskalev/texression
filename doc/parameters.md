# Table parameters

Instance of a class has parameters that influence the generation of the table. 

```python
import texression

tx = texression.texression( varnames = {},          # Human readable variable names
                            varorder = [],          # Ordering, grouping, and hiding of variables
                            maxrows = 100,          # Max number of rows per page
                            head_legend = "",       # Table Head legend
                            adjr2 = False,          # Show adjusted R^2
                            include_std = True,     # Include standard deviation
                            new_str_ex = 3,         # Distance between the rows
                            intertable_fill="",     # Message to display at the next page of a table
                            longtable = False,      # Switch to multi-page table
                            ltcaption = "",         # Caption of the long table
                            ltlabel = "",           # Long table label
                            ltcolwidth = 3,         # Column width for a long table
                            hide_r2fstat = False    # Hide R^2 and F-statistic
                          )
```

+ `varnames` is a dictionary used to convert variable names into human-readable format. Dictionary contains `key : value` pairs, where keys correspond to variable names used in regression model result object and values correspond to human readable names. For example:

```python
varnames = {'t1' : '$Russell 2000_{t}$',
            't0' : '$Russell 2000_{t-1}$',
            'banded' : 'Banded state',
            'banded_t1' : 'Banded state $\\times Russell 2000_{t}$'
           }
```
As these stings are essentially embedded into final LaTeX code, you can use LaTeX code here to aid with mathematical notation.

+ `varorder` is a list that determines the ordering, grouping, and hiding of variables in the table. The elements of the list might be original variable names (strings) or dictionaries that prescribe a certain representation for a set of variables. Three kinds of representations are implemented:

    - **control** variables representation allows researcher to group a set of variables into a "Yes"/"No" indicator that this set is included into the regression model.
    
    - **silent** representation removes enlisted variables from the table.
    
    - **separator** representation allows to split blocks of variables in the table by introducing a sub-header within the table. Please see the [pdf-example](example.pdf).
    
To specify a representation in a dictionary, the following keys are used:

    - *name* - contains human-readable name of the representation in the table.
    - *type* - specifies kind of the representation from the presented above.
    - *vars* - contains a list of original variable names included in the representation.
    
For example:

```python
varorder = ['t1', 't0', 'banded', 'banded_t1',
           {'name' : 'Firm controls', 'type' : 'controls',
            'vars' :['NonIndxOwn', 'ISSrec_For', 'log_atq', 'roa', 'bm_ratio', 'firm_leverage']},
           {'name' : 'Year controls', 'type' : 'controls',
            'vars' : ['y_2010', 'y_2011', 'y_2012', 'y_2013', 'y_2014', 'y_2015', 'y_2016']},
           {'name' : 'Float and mk.cap. controls', 'type' : 'controls',
            'vars' : ['mkcap', 'float_value_t1']},
           {'type' : 'silent', 'vars' : ['const']}]
```

+ `maxrows` is the number of variables to put on a page before a page-split is invoked for multi-page tables.

+ `head_legend` is a legend displayed in the head of the table.

+ `adjr2` add an adjusted R^2 to the table.

+ `include_std` includes standard deviation values into the table.

+ `new_str_ex` adjusts the distance between rows of the table.

+ `intertable_fill` carries a message that will be embedded between tables/pages of a table.

+ `longtable` a toggle betwen `longtable` and `tabular` environments.

+ `ltcaption` is a table's caption in `longtable` environment.

+ `ltlabel` is a label in `longtable` environment.

+ `ltcolwidth` is column width in `longtable` environment.

+ `hide_r2fstat` disables display of R^2 and F statistics.
