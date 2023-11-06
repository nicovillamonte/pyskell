import uuid
import os

class PythonVariables:
  def __init__(self):
    self.id = abs(hash(uuid.uuid4()))
    self.path = f'dist/variables-{self.id}'
    self.values = []
    
    # Si la carpeta dist no existe, la creamos
    if not os.path.exists('dist'):
      os.makedirs('dist')
    
    # create file variables-id in .dist folder
    with open(self.path, 'w') as f:
      f.write('')
  
  def __del__(self):
    os.remove(self.path)
    
  def set_id(self, id):
    self.id = id
    self.path = f'dist/variables-{self.id}'
    # Update the values through file
    self.values = []
    with open(self.path, 'r') as f:
      for line in f:
        value, name, hash = line.split('=')
        self.values.append({
            "name": name,
            "value": value,
            "hash": hash.replace('\n', '')
        })
    
  def add(self, value):
    # value is { "name": left_side.strip(), "value": None, "hash": f"%{str(abs(hash(f'{left_side.strip()}')))}%" }
    with open(self.path, 'a') as f:
      f.write(f'{value["name"]}={value["value"]}={value["hash"]}\n')
      self.values.append(value)
  
  def get_variable(self, hash):
    for variable in self.values:
      if variable["hash"] == hash:
        return variable
    return None
  
  def update(self, value):
    with open(self.path, 'r') as f:
      lines = f.readlines()
    with open(self.path, 'w') as f:
      for line in lines:
        if line.endswith(value["hash"] + '\n'):
          f.write(f'{value["name"]}={value["value"]}={value["hash"]}\n')
          # Change the value in the values list
          for i, variable in enumerate(self.values):
            if variable["hash"] == value["hash"]:
              self.values[i] = value
        else:
          f.write(line)
  
  # Define the __iter__ method
  def __iter__(self):
    self._index = 0  # Initialize a counter for iteration
    return self  # Return the iterator object

  # Define the __next__ method
  def __next__(self):
    if self._index < len(self.values):
      result = self.values[self._index]
      self._index += 1
      return result
    raise StopIteration  # If there are no more items, raise the StopIteration exception
  
  def __len__(self):
    return len(self.values)
    
variables = PythonVariables()
# variables = []


variables_inputs = []
version = "1.0.0"
DEV_MODE = False

command_options = {
  'show_build': '--show-build',         # Show the build process
  'print_assign': '--print-assigns'     # Don't print the assignments
}

options_detail = {
  'show_build': 'Show the build process before run the file.',
  'print_assign': 'Don\'t print the assignments.'
}

execution_config = {
  'assignations_print': True,
}