from quick_find import QuickFind
from quick_union import QuickUnion

def client(*args):
    alg = args[0]
    if alg == "QuickFind":
        impl = QuickFind(10)
    elif alg == "QuickUnion":
        impl = QuickUnion(10)
    impl.union(4, 3)
    impl.union(3, 8)
    impl.union(6, 5)
    impl.union(9, 4)
    impl.union(2, 1)
    print(impl.connected(8, 9))
    print(impl.connected(5, 0))
    impl.union(5, 0)
    impl.union(7, 2)
    impl.union(6, 1)
    impl.union(1, 0)
    print(impl.connected(0, 7))
    print(impl.connected(1, 0))
    print(impl.connected(6, 7))