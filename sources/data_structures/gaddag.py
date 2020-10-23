from enum import Enum

class GADDAG:
    def __init__(self):
        self.root = GADDAG.Node(GADDAG.Node.NodeType.ROOT)

    def __contains__(self, item):
        node = self.root
        #iterate over revese to make it simpler with checking for the word break
        for letter in reversed(item):
            if letter not in node.children:
                return False
            node = node.children[letter]

        return (GADDAG.Node.NodeType.BREAK in node.children) and (GADDAG.Node.NodeType.EOW in node.children[GADDAG.Node.NodeType.BREAK].children)

    def add_word(self, word):
        for index, letter in enumerate(word):
            current_node = self.root
            if letter not in current_node.children:
                current_node.children[letter] = GADDAG.Node(letter)

            current_node = current_node.children[letter]
            prefix = word[:index]
            suffix = word[index+1:]

            for prefix_letter in reversed(prefix):
                if prefix_letter not in current_node.children:
                    current_node.children[prefix_letter] = GADDAG.Node(letter)
                current_node = current_node.children[prefix_letter]

            if GADDAG.Node.NodeType.BREAK not in current_node.children:
                current_node.children[GADDAG.Node.NodeType.BREAK] = GADDAG.Node(GADDAG.Node.NodeType.BREAK)

            current_node = current_node.children[GADDAG.Node.NodeType.BREAK]

            for suffix_letter in suffix:
                if suffix_letter not in current_node.children:
                    current_node.children[suffix_letter] = GADDAG.Node(letter)
                current_node = current_node.children[suffix_letter]

            if GADDAG.Node.NodeType.EOW not in current_node.children:
                current_node.children[GADDAG.Node.NodeType.EOW] = GADDAG.Node(GADDAG.Node.NodeType.EOW)


    def find_matches(self, hook, rack, available_prefix_spaces, available_suffix_spaces):
        if hook is None or len(hook) == 0:
            parent = self.root
        elif hook not in self.root.children:
            return []
        else:
            parent = self.root.children[hook]

        return self.__find_matches(parent, rack, available_prefix_spaces, available_suffix_spaces, [], [], True)


    def __find_matches(self, parent_node, rack, available_prefix_spaces, available_suffix_spaces, current_prefix_letters, current_suffix_letters, is_prepending):
        if is_prepending and available_prefix_spaces < 0 or not is_prepending and available_suffix_spaces < 0:
            return []

        words_in_branch = []
        for candidate in parent_node.children:
            if candidate == GADDAG.Node.NodeType.EOW:
                words_in_branch.append(
                    (
                        ''.join(current_prefix_letters),
                        ''.join(current_suffix_letters)
                    )
                )
            elif candidate == GADDAG.Node.NodeType.BREAK:
                words_in_branch += self.__find_matches(parent_node.children[candidate], rack, available_prefix_spaces, available_suffix_spaces, current_prefix_letters, current_suffix_letters, False)
            elif candidate in rack:
                if is_prepending:
                    new_current_prefix_letters = list(current_prefix_letters)
                    new_current_suffix_letters = current_suffix_letters
                    next_available_prefix_spaces = available_prefix_spaces -1
                    next_available_suffix_spaces = available_suffix_spaces
                    new_current_prefix_letters.insert(0, candidate)
                else:
                    new_current_prefix_letters = current_prefix_letters
                    new_current_suffix_letters = list(current_suffix_letters)
                    next_available_prefix_spaces = available_prefix_spaces
                    next_available_suffix_spaces = available_suffix_spaces - 1
                    new_current_suffix_letters.append(candidate)

                new_rack = list(rack)
                new_rack.remove(candidate)

                words_in_branch += self.__find_matches(parent_node.children[candidate], new_rack, next_available_prefix_spaces, next_available_suffix_spaces, new_current_prefix_letters, new_current_suffix_letters, is_prepending)

        return list(words_in_branch)

    class Node:
        def __init__(self, content):
            self.content = content
            self.children = {}

        class NodeType(Enum):
            ROOT = 0
            EOW = 1
            BREAK = 2
