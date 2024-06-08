import streamlit as st
import pandas as pd
import chardet
from io import BytesIO

CSVfiles = []
xlsxfiles = []

def instructions():
    st.markdown(
        """
        ## Merge CSV Files into One Single File
        - Provide CSV files only.
        - First, give it a list of CSV files, and then it will automatically merge each file into one file.
        - After merging, you can choose to download the merged file as a CSV or TXT file.
        - Support of more  extensions will be added soon.
        """
    )
    st.markdown("---")


def uploadFiles():
    
    selectionBox = st.selectbox("Select Formate",["xlsx","CSV"])
    
    uploadedFile = st.file_uploader("Upload your files here",accept_multiple_files=True)
    
    if selectionBox=="CSV":
        for uploaded in uploadedFile:
            CSVfiles.append(uploaded)
    elif selectionBox == "xlsx":
        for uploaded in uploadedFile:
            xlsxfiles.append(uploaded)
    st.markdown("---")
        
        
instructions()    
uploadFiles()

if CSVfiles:
    
    with st.spinner("Getting Format of the files"):
        result = chardet.detect(CSVfiles[0].getvalue())

        st.write("Detected Encoder: ", result['encoding'])
        
    st.markdown("---")
    
    with st.spinner("Creating List of Data"):
        data = []
        for file in CSVfiles:
            data1 = pd.read_csv(file, delimiter=',', encoding=result['encoding'])
            data.append(data1)
            
    st.markdown("---")
    
    if data:
        mergedData = pd.concat(data, ignore_index=True)
        # Convert DataFrame to CSV
        csv = mergedData.to_csv(index=False)
        txt = mergedData.to_csv(sep='\t', index=False)
        b64_ = BytesIO(csv.encode('utf-8'))
        b64__ = BytesIO(txt.encode('utf-8'))
        # Create download button
        st.download_button(
            label="Download Merged File (CSV)",
            data=b64_,
            file_name="merged_data.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="Download Merged File (TXT)",
            data=b64__,
            file_name="merged_data.txt",
            mime="text/txt"
        )
        
elif xlsxfiles:
    
    with st.spinner("Getting Format of the files"):
        result = chardet.detect(xlsxfiles[0].getvalue())

        st.write("Detected Encoder: ", result['encoding'])
        
    st.markdown("---")
    
    with st.spinner("Creating List of Data"):
        data = []
        for file in xlsxfiles:
            data1 = pd.read_excel(file)
            data.append(data1)
            
    st.markdown("---")
    
    if data:
        mergedData = pd.concat(data, ignore_index=True)
        # Convert DataFrame to CSV
        csv = mergedData.to_csv(index=False)
        txt = mergedData.to_csv(sep='\t', index=False)
        b64_ = BytesIO(csv.encode('utf-8'))
        b64__ = BytesIO(txt.encode('utf-8'))
        # Create download button
        st.download_button(
            label="Download Merged File (CSV)",
            data=b64_,
            file_name="merged_data.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="Download Merged File (TXT)",
            data=b64__,
            file_name="merged_data.txt",
            mime="text/txt"
        )
         
else:
    st.write("No files uploaded yet.")
