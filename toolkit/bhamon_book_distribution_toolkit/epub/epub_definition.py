import abc
from typing import List


class EpubDefinition(abc.ABC):
	

	@abc.abstractmethod
	def list_meta_information_files(self) -> List[str]:
		""" Return source file paths for the meta information files (META-INF) """
