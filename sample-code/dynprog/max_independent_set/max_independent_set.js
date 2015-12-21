"use strict";

var fs = require("fs");

var readInput = function(fileName) {
    var fileContent = fs.readFileSync(fileName, "utf-8");
    var weights = fileContent.trim().split(" ").map(Number);
    return weights;
};

var solve = function(weights) {
    // Remembering the solutions to smaller subproblems.
    var solutions = [];

    // Manually setting the solutions for the smallest possible subproblems.
    solutions[0] = 0;
    solutions[1] = weights[0];

    for (var i = 2; i <= weights.length; i++) {
        // Either current vertex does not belong to the optimal solution...
        var case1Solution = solutions[i - 1];
        // Or it does, then the previous one doesn't.
        var case2Solution = solutions[i - 2] + weights[i - 1];

        // Which option is better?
        solutions[i] = Math.max(case1Solution, case2Solution);
    }

    return {
        maxSum: solutions[solutions.length - 1],
        solutions: solutions
    };
};

var reconstructSolution = function(solutions) {
    var includedItemIndices = [];

    // Starting from the last element and stepping backwards, following the winning case every time.
    var i = solutions.length - 1;
    while (i >= 1) {
        var case1Wins = solutions[i - 1] === solutions[i];
        if (case1Wins) {
            // If case 1 won here, we'll just ignore this item and make 1 step back.
            i--;
        } else {
            // If case 2 won here, we'll remember this item and make 2 steps back.
            includedItemIndices.unshift(i - 1);
            i -= 2;
        }
    }

    return includedItemIndices;
};

var writeOutput = function(result) {
    console.log("--- Weights ---");
    console.log(result.weights);

    console.log("--- Subproblem Solutions ---");
    console.log(result.solutions);

    console.log("--- Indices to Include ---");
    console.log(result.indicesToInclude);

    console.log("--- Max Sum ---");
    console.log(result.maxSum);
};

var weights = readInput("weights01.txt");
var result = solve(weights);
result.weights = weights;
result.indicesToInclude = reconstructSolution(result.solutions);

writeOutput(result);
