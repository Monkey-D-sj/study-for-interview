class StreamTagInterceptor:
	def __init__(self, tag: str):
		self.start_tag = f"<{tag}>"
		self.end_tag = f"</{tag}>"
		self.buffer = ""
		self.printing = False
		self.stopped = False

		# 预计算 end_tag 的所有前缀
		self.end_tag_prefixes = {self.end_tag[:i] for i in
								 range(1,
									   len(self.end_tag) + 1)}

	def feed(self, chunk: str) -> str | None:
		if self.stopped:
			return None

		self.buffer += chunk

		# 未开始打印：检查是否需要开始
		if not self.printing:
			# 找到 start_tag
			if self.start_tag in self.buffer:
				idx = self.buffer.find(self.start_tag)
				# 输出 start_tag 之前的内容
				before = self.buffer[:idx]
				self.buffer = ""
				self.printing = True
				return before
			# 检查 buffer 是否是 start_tag 的前缀
			# 如果不是，说明 buffer 中不可能包含 start_tag，可以安全输出
			elif not any(
					self.start_tag.startswith(p) for p in
					[self.buffer[:i] for i in
					 range(1, len(self.buffer) + 1)]):
				safe = self.buffer
				self.buffer = ""
				return safe
			return None

		# 正在打印：检查是否需要结束
		if self.end_tag in self.buffer:
			idx = self.buffer.find(self.end_tag)
			# 输出 end_tag 之前的内容
			before = self.buffer[:idx]
			self.buffer = ""
			self.stopped = True
			return before

		# 检查 buffer 是否是 end_tag 的前缀
		if self.buffer not in self.end_tag_prefixes:
			# 不是前缀，可以安全输出
			safe = self.buffer
			self.buffer = ""
			return safe

		# 是前缀，继续等待
		return None

	def flush(self) -> str | None:
		if self.buffer and not self.stopped:
			remaining = self.buffer
			self.buffer = ""
			return remaining
		return None