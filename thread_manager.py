"""
Thread Manager Module
Handles multi-threading for mass operations
"""

import threading
import queue
import time
from typing import Callable, List, Any

class ThreadManager:
    def __init__(self):
        self.threads = []
        self.running = False
        self.results = []
        self.errors = []
    
    def run_workers(self, 
                    task_queue: queue.Queue, 
                    worker_func: Callable, 
                    thread_count: int = 10,
                    daemon: bool = True,
                    args: tuple = ()) -> List[threading.Thread]:
        """Run multiple worker threads"""
        self.running = True
        self.threads = []
        self.results = []
        self.errors = []
        
        for i in range(thread_count):
            t = threading.Thread(
                target=self._worker_loop,
                args=(task_queue, worker_func, args),
                daemon=daemon,
                name=f"Worker-{i+1}"
            )
            t.start()
            self.threads.append(t)
        
        return self.threads
    
    def _worker_loop(self, task_queue: queue.Queue, worker_func: Callable, args: tuple):
        """Worker loop for processing tasks"""
        while self.running:
            try:
                task = task_queue.get(timeout=2)
                if task is None:  # Poison pill
                    break
                
                try:
                    result = worker_func(task, *args)
                    self.results.append((task, result, None))
                except Exception as e:
                    self.errors.append((task, str(e)))
                
                task_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                self.errors.append(('worker', str(e)))
                try:
                    task_queue.task_done()
                except:
                    pass
    
    def stop(self):
        """Stop all threads"""
        self.running = False
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=3)
    
    def is_running(self) -> bool:
        return any(t.is_alive() for t in self.threads)
    
    def get_results(self):
        return self.results.copy()
    
    def get_errors(self):
        return self.errors.copy()
    
    def clear(self):
        self.results = []
        self.errors = []
