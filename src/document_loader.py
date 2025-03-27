import os
import tempfile
from langchain_community.document_loaders import CSVLoader, JSONLoader, TextLoader

class DocumentLoader:
    def __init__(self):
        self.loader_config = {
            "txt": TextLoader,
            "csv": CSVLoader,
            "json": JSONLoader,
        }

    def load(self, file):
        """
        Load a single file based on its extension by first storing it temporarily, then using
        the appropriate loader from the loader_config to read the file content.

        Args:
            file: A file object (e.g., from an upload in a web app).

        Returns:
            The loaded document as parsed by the corresponding loader.
        """

        # Create a temporary directory for storing the file
        temp_dir = tempfile.TemporaryDirectory()
        # Create a temporary file path by joining the directory with the uploaded file name
        temp_filepath = os.path.join(temp_dir.name, file.name)

        # Get the file extension to determine the appropriate loader
        file_ext = file.name.split('.')[-1].lower()
        loader = self.loader_config.get(file_ext)

        if not loader:
            raise Exception(f"Unsupported file extension: {file_ext}")

        # Write the file's content to the temporary file (in binary mode)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())

        if file_ext == 'json':
            loader = loader(
                file_path=temp_filepath,
                jq_schema='.',              # JSON query schema (default is full document)
                text_content=False          # Specify whether to extract content as plain text
            )
        else:
            loader = loader(temp_filepath)

        return loader.load()

    def load_multiples(self, files):
        """
        Load multiple files by iterating through each one, processing them with the load() method,
        and then combining their contents into a single list.

        Args:
            files: A list of file objects.

        Returns:
            A list of documents loaded from all the files.
        """
        docs = []

        for file in files:
            doc = self.load(file)
            docs.extend(doc)

        return docs
