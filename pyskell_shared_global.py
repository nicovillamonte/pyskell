import uuid
import os
from threading import Semaphore as ThreadSemaphore
from multiprocessing import Semaphore as ProcessSemaphore

class PythonVariables:
  def __init__(self):
    self.id = abs(hash(uuid.uuid4()))
    self.path = f'dist/variables-{self.id}'
    self.thread_sem = ThreadSemaphore()
    self.process_sem = ProcessSemaphore()
    self._variables_cache = None
    
    # Si la carpeta dist no existe, la creamos
    if not os.path.exists('dist'):
      os.makedirs('dist')
    
    # create file variables-id in .dist folder
    with open(self.path, 'w') as f:
      f.write('')
  
  # def __del__(self):
  #   if os.path.exists(self.path):  # Verificar si el archivo existe antes de intentar eliminarlo
  #       os.remove(self.path)
  
  def start_action(self):
    self.thread_sem.acquire()
    self.process_sem.acquire()
  
  def end_action(self):
    self.thread_sem.release()
    self.process_sem.release()
    
  def set_id(self, id):
    os.remove(self.path)
    self.id = id
    self.path = f'dist/variables-{self.id}'
    
  def add(self, value): # Only used in the builder
    self.start_action()
    exists = False
    with open(self.path, 'r+') as f:  # Open the file for reading and writing.
        lines = f.readlines()  # Read all the lines.
        for line in lines:
            name, _, _ = line.split('=')
            if name == value["name"]:
                exists = True
                break
        if not exists:
            f.seek(0, os.SEEK_END)  # Move the pointer to the end of the file.
            f.write(f'{value["name"]}={value["value"]}={value["hash"]}\n')  # Write the new entry.
    self.end_action()
  
  def get_variables(self):
    self.start_action()
    try:
        variables = []
        with open(self.path, 'r') as f:
            for line in f:
                name, value, hash = line.strip().split('=')
                variables.append({
                    "name": name,
                    "value": value,
                    "hash": hash
                })
    except Exception as e:
        # Aquí deberías manejar el error, como logearlo o relanzar la excepción.
        raise e
    finally:
        self.end_action()
    return variables

  # def get_variables(self):
  #   self.start_action()
  #   variables = []
  #   with open(self.path, 'r') as f:
  #     for line in f:
  #       name, value, hash = line.split('=')
  #       variables.append({
  #         "name": name,
  #         "value": value,
  #         "hash": hash.replace('\n', '')
  #       })
  #   self.end_action()
  #   return variables
  
  def get_variable(self, hash):
    self.start_action()
    output = None
    with open(self.path, 'r') as f:
      for line in f:
        name, value, hash_ = line.split('=')
        if hash == hash_.replace('\n', ''):
          output = {
            "name": name,
            "value": value,
            "hash": hash_.replace('\n', '')
          }
          break
    self.end_action()
    return output
  
  def update(self, value):
    self.start_action()
    with open(self.path, 'r+') as f:
      lines = f.readlines()
      f.seek(0)
      f.truncate()
      updated = False
      for line in lines:
        name, _, hash_ = line.split('=')
        hash = hash_.replace('\n', '')
        if hash == value["hash"]:
          f.write(f'{value["name"]}={value["value"]}={value["hash"]}\n')
          updated = True
        else:
          f.write(line)  # Asegúrate de agregar '\n' para mantener la estructura de líneas
    self.end_action()
  
  def __iter__(self):
    if self._variables_cache is None:
      self._variables_cache = self.get_variables()  # Solo se llama una vez y se almacena en caché.
      self._index = 0
    return self

  def __next__(self):
    if self._index < len(self._variables_cache):
      result = self._variables_cache[self._index]
      self._index += 1
      return result
    else:
      self._variables_cache = None  # Resetear el caché después de la iteración
      raise StopIteration
  
  def __len__(self):
    vars = self.get_variables()
    return len(vars)
    
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