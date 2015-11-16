using System;

namespace BinaryHeap
{
    class Program
    {
        public static void Main(string[] args)
        {
            var array = GenerateRandomArray();
            HeapSort(array);

            foreach (var item in array)
            {
                Console.WriteLine(item);
            }
        }

        private static int[] GenerateRandomArray()
        {
            Random randomGenerator = new Random();
            int[] array = new int[100];

            for (int i = 0; i < array.Length; i++)
            {
                array[i] = randomGenerator.Next(1, 50);
            }

            return array;
        }

        private static void HeapSort(int[] array)
        {
            var heap = new BinaryMinHeap<int>(array.Length);
            foreach (var item in array)
            {
                heap.Add(item);
            }
            for (int i = 0; i < array.Length; i++)
            {
                array[i] = heap.RemoveMin();
            }
        }
    }

    public class BinaryMinHeap<TKey> where TKey: IComparable
    {
        private TKey[] _items;

        private int _currentSize;


        public int CurrentSize
        {
            get { return _currentSize; }
        }


        public BinaryMinHeap(int capacity)
        {
            _items = new TKey[capacity];
        }


        public void Add(TKey item)
        {
            if (_currentSize == _items.Length)
            {
                throw new InvalidOperationException("Heap capacity exceeded. Cannot add new item.");
            }

            _items[_currentSize] = item;
            _currentSize++;
            BubbleUp(_currentSize - 1);
        }

        public TKey Peek()
        {
            if (_currentSize == 0)
            {
                throw new InvalidOperationException("Cannot peek when the heap is empty.");
            }

            return _items[0];
        }

        public TKey RemoveMin()
        {
            if (_currentSize == 0)
            {
                throw new InvalidOperationException("Cannot remove when the heap is empty.");
            }

            TKey min = _items[0];
            Swap(0, _currentSize - 1);
            _currentSize--;
            BubbleDown(0);

            return min;
        }

        private void BubbleUp(int index)
        {
            while (CompareAndSwapWithParentIfNecessary(index))
            {
                index = GetParentIndex(index);
            }
        }

        private void BubbleDown(int index)
        {
            if (!HasChildren(index))
            {
                return;
            }

            int bestChildIndex = GetBestChildIndex(index);
            if (CompareAndSwapWithParentIfNecessary(bestChildIndex))
            {
                BubbleDown(bestChildIndex);
            }
        }

        private bool CompareAndSwapWithParentIfNecessary(int childIndex)
        {
            if (childIndex == 0)
            {
                return false;
            }

            int parentIndex = GetParentIndex(childIndex);
            if (GetBestIndex(parentIndex, childIndex) == childIndex)
            {
                Swap(parentIndex, childIndex);
                return true;
            }
            return false;
        }

        private int GetBestIndex(int index1, int index2)
        {
            bool item1IsBetter = _items[index1].CompareTo(_items[index2]) < 0;
            return item1IsBetter ? index1 : index2;
        }

        private int GetBestChildIndex(int parentIndex)
        {
            int leftChildIndex = GetLeftChildIndex(parentIndex);
            int rightChildIndex = GetRightChildIndex(parentIndex);

            if (ItemExists(rightChildIndex))
            {
                return GetBestIndex(leftChildIndex, rightChildIndex);
            }

            return leftChildIndex;
        }

        private bool HasChildren(int index)
        {
            return ItemExists(GetLeftChildIndex(index));
        }

        private bool ItemExists(int index)
        {
            return index < _currentSize;
        }

        private void Swap(int index1, int index2)
        {
            TKey temp = _items[index1];
            _items[index1] = _items[index2];
            _items[index2] = temp;
        }

        private int GetParentIndex(int childIndex)
        {
            return (childIndex - 1) / 2;
        }

        private int GetLeftChildIndex(int parentIndex)
        {
            return 2 * parentIndex + 1;
        }

        private int GetRightChildIndex(int parentIndex)
        {
            return 2 * parentIndex + 2;
        }
    }
}
