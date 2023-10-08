"""
Given n pairs of parentheses, write a function to generate all combinations of well formed parentheses.

Example 1:

Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]


Example 2:

Input: n = 1
Output: ["()"]


Example 3: 

Input: n = 2
Output: ["()()", "(())"]

f(1) = ["()"]
f(2) = [f(1) + f(1), "(", f(1), ")"]

genParens(n, l, r):
  # if n == 0:
  #   return ""
  # else: 
  #   return [
  #     f(n - 1) + f(n - 1),
  #     "(" + f(n - 1) + ")",
  #     ")("
  #   ]
  if l:
    return genParens(')', n -1, r)
  elif l < r:
    return genParens(')', n

  return genParens('', n, n)


3
f(0) = ""
f(1) = "()"
f(2) = "()"+"()", "("+"()"+")"
f(3) = "()"+"()"+"()", "("+"()"+")" 


n * "(" + n * ")"
n * "()"

output = []
iterate n:
  for l, r in output:
    
"""


# Bottom up DP
def genParensDp(n):
    dp = [[] for i in range(n + 1)]
    dp[0].append("")

    for i in range(n + 1):
        for j in range(i):
            # n = 3
            # [''], ['()'], ['()()', '(())'], ['()']
            for y in dp[i - j - 1]:
                for x in dp[j]:
                    print(i, j, x, y)
                    dp[i] += "(" + x + ")" + y

            # dp[i] += ["(" + x + ")" + y for x in dp[j] for y in dp[i - j - 1]]

    return dp[n]


# Top down DP
def genParensRecur(n):
    res = []

    def dfs(left, right, s):
        if len(s) == n * 2:
            res.append(s)
            return

        if left < n:
            dfs(left + 1, right, s + "(")

        if right < left:
            dfs(left, right + 1, s + ")")

    dfs(0, 0, "")
    return res


if __name__ == "__main__":
    genParensDp(2)
