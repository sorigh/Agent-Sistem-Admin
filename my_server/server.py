from fastmcp import FastMCP
from fastapi import Request, Response
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated
import os
import logging 
mcp = FastMCP("My MCP Server")

FLAG_FILENAME = "flag.txt"

@mcp.tool()
def list_directory(directory: str = None) -> list[str]:
    """
    List all files and directories in the given directory.
    
    Args:
        directory_path: The absolute or relative path to the directory. (example: '.' or 'home/user/docs').
    """
    try:
        items = os.listdir(directory)
        secure_items = [item for item in items if item.lower() != FLAG_FILENAME.lower()]
        return secure_items
    except Exception as e:
        logging.error(f"Error listing directory {directory}: {e}")
        return [f"Error: {str(e)}"]

@mcp.tool()
def get_file_content(dir_path: str = None) -> str:
    """
    Reads and returns the full text content of a specified file.
    BLOCKS access to the flag file.
    Args:
        file_path: The full path to the file you want to read (example: 'src/main.py').
    """
    # condition for flag file access
    try:
        abs_path = os.path.abspath(dir_path)
        filename = os.path.basename(abs_path)
        if filename.lower() == FLAG_FILENAME.lower():
            return "ACCESS DENIED: This file is protected. Use 'verify_flag' to check its content."
        
        # 4. Double Check: Ensure we aren't resolving a symlink that points to the flag
        # (Optional but recommended for high security)
        real_path = os.path.realpath(dir_path)
        if os.path.basename(real_path).lower() == FLAG_FILENAME.lower():
             return "ACCESS DENIED: Protected file detected."


        with open(dir_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        logging.error(f"Error reading file {dir_path}: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def write_file(file_path: str, content: str = None) -> str:
    """
    Writes or overwrites content to a specified file.
    
    Args:
        file_path: The full path to the file you want to write to (example: 'files/notes.txt').
        content: The text content to write into the file.
    """
    try:
        if os.path.basename(file_path).lower() == FLAG_FILENAME.lower():
            return "Error: Cannot overwrite protected system files."
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote content to {file_path}"
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        return f"Error: {str(e)}"
    

@mcp.tool()
def create_directory(directory_path: str = None) -> str:
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
def delete_file(file_path: str = None) -> str:
    """
    Deletes a specified file. Should be used with caution.
    
    Args:
        file_path: The full path to the file you want to delete.
    """
    try:
        if os.path.basename(file_path).lower() == FLAG_FILENAME.lower():
            return "Error: Cannot delete protected system files."
        os.remove(file_path)
        return f"Successfully deleted file {file_path}"
    except Exception as e:
        logging.error(f"Error deleting file {file_path}: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
def verify_flag(guess: str) -> str:
    """
    Verifies if the provided text matches the secret flag content.
    Returns "True" or "False".
    
    Args:
        guess: The text to compare against the flag.
    """
    try:
        # Assuming flag.txt is in the current working directory of the server
        # You might need to adjust the path depending on where you put the file
        if not os.path.exists(FLAG_FILENAME):
             return "Error: Flag file not found on system."
             
        with open(FLAG_FILENAME, 'r') as f:
            real_flag = f.read().strip()
            
        if guess.strip() == real_flag:
            return "True"
        else:
            return "False"
    except Exception as e:
        return f"Error verifying flag: {str(e)}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    mcp.run(transport="http", host="0.0.0.0", port=8100)
