# CSVFilter

CSVFilter is a web application that allows users to filter and sort data from CSV files easily. With a simple and intuitive interface, you can quickly find the data you need and download the filtered results.

## Features

- **Upload CSV Files:** Easily upload your CSV files to the application.
- **Filter Data:** Select specific columns and values to filter the data.
- **Sort Data:** Order the filtered data by any column.
- **Download Results:** Download the filtered and sorted data as a new CSV file.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Flask
- Pandas

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/l364cyx/CSVFilter.git
   ```
2. **Build:**
   ```sh
   cd csvfilter
   docker build . -t csvfilter
   ```
3. **Deploy:**
   ```sh
   docker run --rm -d -p 5000:5000 csvfilter
   ```