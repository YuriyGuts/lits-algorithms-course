package com.lits.ads002;

import java.util.Arrays;

public class Main {

    public static void main(String[] args) {
        Integer[] array = { 5, 13, 6, 3, 1, 5, 6, 7, 89, 9, 64 };
        mergeSort(array);
        System.out.println(Arrays.toString(array));
    }

    private static void mergeSort(Comparable[] array) {
        Comparable[] mergeResults = new Comparable[array.length];
        mergeSortRecursive(array, mergeResults, 0, array.length - 1);
    }

    private static void mergeSortRecursive(Comparable[] array, Comparable[] mergeResults, int left, int right) {
        if (left < right) {
            int center = (left + right) / 2;
            mergeSortRecursive(array, mergeResults, left, center);
            mergeSortRecursive(array, mergeResults, center + 1, right);
            merge(array, mergeResults, left, center + 1, right);
        }
    }

    private static void merge(Comparable[] array, Comparable[] mergeResults, int leftBegin, int rightBegin, int rightEnd) {
        int leftEnd = rightBegin - 1;
        int leftReadPos = leftBegin;
        int rightReadPos = rightBegin;
        int resultWritePos = leftBegin;

        while (leftReadPos <= leftEnd && rightReadPos <= rightEnd) {
            if (array[leftReadPos].compareTo(array[rightReadPos]) < 0) {
                mergeResults[resultWritePos++] = array[leftReadPos++];
            } else {
                mergeResults[resultWritePos++] = array[rightReadPos++];
            }
        }

        while (leftReadPos <= leftEnd) {
            mergeResults[resultWritePos++] = array[leftReadPos++];
        }

        while (rightReadPos <= rightEnd) {
            mergeResults[resultWritePos++] = array[rightReadPos++];
        }

        for (int i = leftBegin; i <= rightEnd; i++) {
            array[i] = mergeResults[i];
        }
    }
}
