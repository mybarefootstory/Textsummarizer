import os
from urllib import request
import zipfile
from src.Text_Summarizer.logging import logger
from src.Text_Summarizer.entity import DataIngestionConfig
import re


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"File downloaded from {self.config.source_URL} to {self.config.local_data_file}")
        else:
            logger.info("File already exists")

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory with sanitized filenames for Windows
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        
        # First, let's check what's inside the zip file
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            # List all files in the zip to debug
            logger.info("Files in the zip archive:")
            for name in zip_ref.namelist()[:10]:  # Show first 10 files
                logger.info(f"  {name}")
            
            # Extract with sanitization
            for member_info in zip_ref.infolist():
                # Sanitize the filename by replacing problematic characters
                # Common issue: Hugging Face datasets often use colons in paths
                sanitized_name = member_info.filename
                
                # Replace colons and other Windows-illegal characters
                sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', sanitized_name)
                
                # Construct the target path
                target_path = os.path.join(unzip_path, sanitized_name)
                
                # If it's a directory, create it
                if member_info.is_dir() or member_info.filename.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    # Ensure parent directory exists
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    
                    # Extract the file
                    try:
                        with zip_ref.open(member_info) as source:
                            with open(target_path, "wb") as target:
                                target.write(source.read())
                    except Exception as e:
                        logger.error(f"Failed to extract {member_info.filename}: {e}")
                        logger.error(f"Target path was: {target_path}")
                        raise
        
        logger.info(f"Zip file extracted to {unzip_path}")