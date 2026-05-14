"""
Automated Tests & Benchmarks for DSA Explorer
Covers Stack, Queue, Linked List, BST (Phases 1–3)
"""

import unittest
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.stack import Stack
from modules.queue_ds import Queue


# ─── Linked List (inline for testing) ────────────────────────────────────────

class LLNode:
    def __init__(self, v): self.value = v; self.next = None

class LinkedList:
    def __init__(self): self.head = None
    def append(self, v):
        n = LLNode(v)
        if not self.head: self.head = n; return
        cur = self.head
        while cur.next: cur = cur.next
        cur.next = n
    def insert_at(self, pos, v):
        n = LLNode(v)
        if pos == 0: n.next = self.head; self.head = n; return True
        cur, idx = self.head, 0
        while cur and idx < pos - 1: cur = cur.next; idx += 1
        if not cur: return False
        n.next = cur.next; cur.next = n; return True
    def to_list(self):
        res, cur = [], self.head
        while cur: res.append(cur.value); cur = cur.next
        return res
    def reverse(self):
        prev, cur = None, self.head
        while cur: nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        self.head = prev

# ─── BST (inline for testing) ─────────────────────────────────────────────────

class BSTNode:
    def __init__(self, v): self.value = v; self.left = self.right = None

class BST:
    def __init__(self): self.root = None
    def insert(self, v):
        def _ins(n, v):
            if not n: return BSTNode(v)
            if v < n.value: n.left = _ins(n.left, v)
            elif v > n.value: n.right = _ins(n.right, v)
            return n
        self.root = _ins(self.root, v)
    def inorder(self):
        res = []
        def _in(n):
            if n: _in(n.left); res.append(n.value); _in(n.right)
        _in(self.root); return res
    def search(self, v):
        cur = self.root
        while cur:
            if v == cur.value: return True
            cur = cur.left if v < cur.value else cur.right
        return False


# ══════════════════════════════════════════════════════════════════════════════
# STACK TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestStack(unittest.TestCase):

    def test_push_pop_sequence(self):
        """Push 3 items, pop 2 — final size should be 1, correct order."""
        s = Stack()
        s.push(10); s.push(20); s.push(30)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.pop(), 30)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.peek(), 10)

    def test_push_pop_large(self):
        """Push 1000 items, verify LIFO order."""
        s = Stack()
        for i in range(1000): s.push(i)
        self.assertEqual(s.size(), 1000)
        for i in reversed(range(1000)):
            self.assertEqual(s.pop(), i)
        self.assertTrue(s.is_empty())

    def test_peek_does_not_remove(self):
        s = Stack(); s.push(42)
        self.assertEqual(s.peek(), 42)
        self.assertEqual(s.size(), 1)

    def test_exceptions(self):
        s = Stack()
        with self.assertRaises(IndexError): s.pop()
        with self.assertRaises(IndexError): s.peek()

    def test_benchmark(self):
        """Benchmark: push/pop 1,000,000 items — should complete < 5s."""
        s = Stack()
        n = 1_000_000
        start = time.time()
        for i in range(n): s.push(i)
        for i in range(n): s.pop()
        elapsed = time.time() - start
        print(f"\n  [Benchmark] Stack push/pop {n:,} items: {elapsed:.4f}s")
        self.assertLess(elapsed, 5.0)


# ══════════════════════════════════════════════════════════════════════════════
# QUEUE TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestQueue(unittest.TestCase):

    def test_fifo_order(self):
        """Enqueue 4 items, dequeue 3 — FIFO order maintained."""
        q = Queue()
        for v in [10, 20, 30, 40]: q.enqueue(v)
        self.assertEqual(q.dequeue(), 10)
        self.assertEqual(q.dequeue(), 20)
        self.assertEqual(q.dequeue(), 30)
        self.assertEqual(q.size(), 1)
        self.assertEqual(q.peek(), 40)

    def test_empty_exceptions(self):
        q = Queue()
        with self.assertRaises(IndexError): q.dequeue()
        with self.assertRaises(IndexError): q.peek()

    def test_size_tracking(self):
        q = Queue()
        for i in range(10): q.enqueue(i)
        self.assertEqual(q.size(), 10)
        q.dequeue(); q.dequeue()
        self.assertEqual(q.size(), 8)

    def test_benchmark(self):
        """Benchmark: enqueue/dequeue 1,000,000 items."""
        q = Queue()
        n = 1_000_000
        start = time.time()
        for i in range(n): q.enqueue(i)
        for i in range(n): q.dequeue()
        elapsed = time.time() - start
        print(f"\n  [Benchmark] Queue enqueue/dequeue {n:,} items: {elapsed:.4f}s")
        self.assertLess(elapsed, 5.0)


# ══════════════════════════════════════════════════════════════════════════════
# LINKED LIST TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestLinkedList(unittest.TestCase):

    def test_append_and_traverse(self):
        ll = LinkedList()
        for v in [10, 20, 30]: ll.append(v)
        self.assertEqual(ll.to_list(), [10, 20, 30])

    def test_insert_at_position(self):
        """Insert node with value 10 at position 2."""
        ll = LinkedList()
        ll.append(1); ll.append(2); ll.append(3)
        ll.insert_at(2, 10)
        self.assertEqual(ll.to_list(), [1, 2, 10, 3])

    def test_insert_at_head(self):
        ll = LinkedList()
        ll.append(5); ll.append(6)
        ll.insert_at(0, 99)
        self.assertEqual(ll.to_list(), [99, 5, 6])

    def test_reverse(self):
        ll = LinkedList()
        for v in [1, 2, 3, 4, 5]: ll.append(v)
        ll.reverse()
        self.assertEqual(ll.to_list(), [5, 4, 3, 2, 1])


# ══════════════════════════════════════════════════════════════════════════════
# BST TESTS
# ══════════════════════════════════════════════════════════════════════════════

class TestBST(unittest.TestCase):

    def test_insert_inorder(self):
        """Insert [50,30,70]; inorder should give [30,50,70]."""
        bst = BST()
        for v in [50, 30, 70]: bst.insert(v)
        self.assertEqual(bst.inorder(), [30, 50, 70])

    def test_search_found(self):
        bst = BST()
        for v in [50, 30, 70, 20, 40]: bst.insert(v)
        self.assertTrue(bst.search(40))
        self.assertFalse(bst.search(99))

    def test_inorder_sorted(self):
        """Inorder of a BST is always sorted."""
        bst = BST()
        values = [45, 12, 78, 3, 33, 60, 90]
        for v in values: bst.insert(v)
        result = bst.inorder()
        self.assertEqual(result, sorted(values))

    def test_benchmark(self):
        """Benchmark: insert 10,000 items into BST."""
        import random
        bst = BST()
        values = random.sample(range(1, 100_001), 10_000)
        start = time.time()
        for v in values: bst.insert(v)
        elapsed = time.time() - start
        print(f"\n  [Benchmark] BST insert 10,000 items: {elapsed:.4f}s")
        self.assertLess(elapsed, 2.0)


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
