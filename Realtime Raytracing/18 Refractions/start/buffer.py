from config import *

class Buffer:

    def __init__(self, size: int, binding: int, floatCount: int, dtype: np.dtype):

        self.size = size
        self.binding = binding
        self.floatCount = floatCount

        self.hostMemory = np.zeros(floatCount * size, dtype=dtype)

        self.deviceMemory = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMemory)
        glBufferStorage(
            GL_SHADER_STORAGE_BUFFER, self.hostMemory.nbytes, 
            self.hostMemory, GL_DYNAMIC_STORAGE_BIT)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding, self.deviceMemory)
        self.elements_updated = 0
    
    def blit(self, data: np.ndarray) -> None:

        self.hostMemory[:] = data[:self.size*self.floatCount]

        self.elements_updated = self.size   
    
    def readFrom(self) -> None:
        """
            Upload the CPU data to the buffer, then arm it for reading.
        """

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMemory)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.floatCount * 4 * self.elements_updated, self.hostMemory)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, self.binding, self.deviceMemory)
        self.elements_updated = 0
    
    def destroy(self) -> None:
        """
            Free the memory.
        """

        glDeleteBuffers(1, (self.deviceMemory,))