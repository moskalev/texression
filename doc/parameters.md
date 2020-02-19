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

`varnames` is a dictionary used to convert variable names into human-readable format.

`varorder` is a list that determines the ordering, grouping, and hiding of variables in the table.

`maxrows` is the number of variables to put on a page before a page-split is invoked for multi-page tables.

`head_legend` is a legend displayed in the head of the table.

`adjr2` add an adjusted R^2 to the table.

`include_std` includes standard deviation values into the table.

`new_str_ex` adjusts the distance between rows of the table.

`intertable_fill` carries a message that will be embedded between tables/pages of a table.

`longtable` a toggle betwen `longtable` and `tabular` environments.

`ltcaption` is a table's caption in `longtable` environment.

`ltlabel` is a label in `longtable` environment.

`ltcolwidth` is column width in `longtable` environment.

`hide_r2fstat` disables display of R^2 and F statistics.
