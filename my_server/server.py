from fastmcp import FastMCP
from fastapi import Header, HTTPException
from typing import Annotated
import os
import logging

mcp = FastMCP("My MCP Server")


def verify_key(key: str | None):
    expected_key = os.getenv("MCP_API_KEY")
    if not expected_key:
        return True # Sau False dacă vreți să forțați auth chiar dacă lipsesc env vars
    if key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@mcp.tool()
def list_directory(directory: str, x_api_key: Annotated[str | None, Header()] = None) -> list[str]:
    """
    List all files and directories in the given directory.
    
    Args:
        directory_path: The absolute or relative path to the directory. (example: '.' or 'home/user/docs').
    """
    try:
        items = os.listdir(directory)
        return items
    except Exception as e:
        logging.error(f"Error listing directory {directory}: {e}")
        return [f"Error: {str(e)}"]

@mcp.tool()
def get_file_content(dir_path: str, x_api_key: Annotated[str | None, Header()] = None) -> str:
    """
    Reads and returns the full text content of a specified file.
    
    Args:
        file_path: The full path to the file you want to read (example: 'src/main.py').
    """
    try:
        with open(dir_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        logging.error(f"Error reading file {dir_path}: {e}")
        return f"Error: {str(e)}"
    
@mcp.tool()
def write_file(file_path: str, content: str, x_api_key: Annotated[str | None, Header()] = None) -> str:
    """
    Writes or overwrites content to a specified file.
    
    Args:
        file_path: The full path to the file you want to write to (example: 'files/notes.txt').
        content: The text content to write into the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote content to {file_path}"
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        return f"Error: {str(e)}"
    

@mcp.tool()
def create_directory(directory_path: str, x_api_key: Annotated[str | None, Header()] = None) -> str:
    """
    Creates a new directory at the specified path.
    
    Args:
        directory_path: The path where the new directory should be created (example: 'new_project/src').
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return f"Successfully created directory {directory_path}"
    except Exception as e:
        logging.error(f"Error creating directory {directory_path}: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def delete_file(file_path: str, x_api_key: Annotated[str | None, Header()] = None) -> str:
    """
    Deletes a specified file. Should be used with caution.
    
    Args:
        file_path: The full path to the file you want to delete.
    """
    try:
        os.remove(file_path)
        return f"Successfully deleted file {file_path}"
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {e}")
        return f"Error: {str(e)}"
    

if __name__ == "__main__":
    
    mcp.run(transport="http", host="0.0.0.0", port=8100)
