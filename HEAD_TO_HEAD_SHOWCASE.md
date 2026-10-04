# Head-to-Head Showcase: Base Model vs. DataMind-3B

> **Direct Side-by-Side Code Output Comparison**  
> Evaluated on a 4GB VRAM laptop using Ollama (sequential VRAM-safe execution).

---

## Challenge 1: SQL Dynamic Pivot & CTEs

**Prompt Given to Both Models:**
> *"Write a SQL query using CTEs to pivot monthly sales data so that months (Jan, Feb, Mar) become columns for each sales rep dynamically."*

### 🔴 Base Model (`Qwen2.5-Coder-3B`)
*Generation Time: 76.06s*

To pivot monthly sales data using Common Table Expressions (CTEs) in SQL, you can use the `PIVOT` clause. However, since SQL Server does not support the `PIVOT` clause directly, you can achieve this by using a combination of `UNION ALL` and `CASE` statements. Below is an example of how you can write such a query:

Assume you have a table named `SalesData` with the following columns: `SalesRep`, `Month`, and `SalesAmount`.

```sql
WITH MonthlySales AS (
    SELECT 
        SalesRep,
        Month,
        SalesAmount
    FROM 
        SalesData
),
PivotedSales AS (
    SELECT 
        SalesRep,
        Jan = SUM(CASE WHEN Month = 'Jan' THEN SalesAmount ELSE 0 END),
        Feb = SUM(CASE WHEN Month = 'Feb' THEN SalesAmount ELSE 0 END),
        Mar = SUM(CASE WHEN Month = 'Mar' THEN SalesAmount ELSE 0 END)
    FROM 
        MonthlySales
    GROUP BY 
        SalesRep
)
SELECT * FROM PivotedSales;
```

### Explanation:

1. **MonthlySales CTE**: This CTE selects the `SalesRep`, `Month`, and `SalesAmount` from the `SalesData` table.

2. **PivotedSales CTE**: This CTE uses `UNION ALL` to create a new row for each sales rep for each month. It uses `CASE` statements to sum the `SalesAmount` for each month. If a sales rep does not have sales for a particular month, the sum is `0`.

3. **Final SELECT**: The final query selects all columns from the `PivotedSales` CTE, which now has the sales data pivoted into columns for each month.

This query will dynamically pivot the sales data based on the months available in the `SalesData` table. If you have a different set of months or additional sales reps, you can modify the `CASE` statements accordingly.

---

### 🟢 Fine-Tuned Model (`DataMind-3B`)
*Generation Time: 41.96s*

Assuming you have a table `sales` with columns `rep_id`, `month`, and `sales_amount`, the following SQL query can be used to pivot the data:

```sql
WITH MonthlySales AS (
    SELECT 
        rep_id,
        month,
        sales_amount
    FROM 
        sales
),
PivotedSales AS (
    SELECT 
        rep_id,
        [Jan],
        [Feb],
        [Mar]
    FROM 
        MonthlySales
    PIVOT (
        SUM(sales_amount)
        FOR month IN ([Jan], [Feb], [Mar])
    ) AS PivotTable
)
SELECT * FROM PivotedSales;
```

This query first creates a CTE `MonthlySales` to select the relevant columns from the original table. Then, it creates another CTE `PivotedSales` to pivot the data. The `PIVOT` operator is used to transform the rows into columns based on the `month` column. Finally, the results are selected from the `PivotedSales` CTE.

Please note that this query assumes that the months are represented as strings ('Jan', 'Feb', 'Mar') in the original table. If they are represented as numbers or dates, you may need to adjust the query accordingly.

---

## Challenge 2: 50GB Big Data Memory Chunking in Pandas

**Prompt Given to Both Models:**
> *"Write a Python script to process a 50GB CSV file in chunks using Pandas, calculate the total revenue grouped by 'Category', and combine the results efficiently without running out of memory."*

### 🔴 Base Model (`Qwen2.5-Coder-3B`)
*Generation Time: 30.42s*

To process a large CSV file efficiently in chunks using Pandas and calculate the total revenue grouped by 'Category', you can follow these steps:

1. **Read the CSV file in chunks**: Use the `chunksize` parameter in `pd.read_csv()` to read the file in manageable parts.
2. **Calculate the total revenue for each chunk**: For each chunk, calculate the total revenue by summing the 'Revenue' column.
3. **Combine the results**: Use the `concat` function to combine the results from all chunks into a single DataFrame.
4. **Group by 'Category' and calculate the total revenue**: Use the `groupby` method to group the combined DataFrame by 'Category' and calculate the total revenue for each group.

Here's a Python script that implements these steps:

```python
import pandas as pd

# Define the path to your CSV file
file_path = 'path_to_your_50gb_csv_file.csv'

# Define the chunk size
chunk_size = 1000000  # Adjust this value based on your memory capacity

# Initialize an empty list to store the results
results = []

# Read the CSV file in chunks
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    # Calculate the total revenue for the current chunk
    total_revenue = chunk['Revenue'].sum()
    
    # Create a dictionary with the results for the current chunk
    chunk_results = {
        'Category': chunk['Category'].iloc[0],  # Assuming 'Category' is the first column
        'Total_Revenue': total_revenue
    }
    
    # Append the results to the list
    results.append(chunk_results)

# Combine the results into a single DataFrame
combined_results = pd.DataFrame(results)

# Group by 'Category' and calculate the total revenue
grouped_results = combined_results.groupby('Category')['Total_Revenue'].sum().reset_index()

# Display the grouped results
print(grouped_results)
```

### Key Points:
- **Chunk Size**: Adjust the `chunk_size` based on your available memory. A smaller chunk size will use less memory but may require more iterations to process the entire file.
- **Memory Management**: Ensure that your system has enough memory to handle the chunks. If memory is an issue, consider using a more efficient data structure or processing the data in smaller batches.
- **Data Types**: Ensure that the 'Revenue' column is of a numeric type to avoid errors during summation.

This script will efficiently process the large CSV file in chunks, calculate the total revenue for each category, and output the results in a DataFrame.

---

### 🟢 Fine-Tuned Model (`DataMind-3B`)
*Generation Time: 19.72s*

Here is a Python script that processes a 50GB CSV file in chunks using Pandas, calculates the total revenue grouped by 'Category', and combines the results efficiently without running out of memory.

```python
import pandas as pd

# Define the path to the CSV file
file_path = 'path_to_your_50gb_csv_file.csv'

# Initialize an empty DataFrame to store the results
results = pd.DataFrame()

# Set the chunk size
chunk_size = 1000000

# Process the CSV file in chunks
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    # Calculate the total revenue grouped by 'Category'
    total_revenue = chunk.groupby('Category')['Revenue'].sum()
    
    # Append the results to the DataFrame
    results = results.append(total_revenue)

# Display the results
print(results)
```

In this script, we first import the Pandas library. We then define the path to the CSV file and initialize an empty DataFrame to store the results.

Next, we set the chunk size to 1 million rows. This means that each chunk will contain 1 million rows of data.

We then use a for loop to process the CSV file in chunks. For each chunk, we calculate the total revenue grouped by 'Category' using the `groupby` and `sum` methods. The results are appended to the `results` DataFrame.

Finally, we display the results using the `print` function.

This script efficiently processes the 50GB CSV file in chunks without running out of memory.

---

