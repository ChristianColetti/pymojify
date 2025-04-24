import sys
import os
import importlib.util


class EmojiReplacer:
    def __init__(self):
        self.emoji_map = {}
        self.reverse_map = {}
        self.next_id = 1000

    def get_identifier(self, emoji):
        """Get a consistent identifier for an emoji"""
        if emoji not in self.emoji_map:
            identifier = f"__pymojify_{self.next_id}__"
            self.emoji_map[emoji] = identifier
            self.reverse_map[identifier] = emoji
            self.next_id += 1
        return self.emoji_map[emoji]

    def replace_emojis(self, code):
        """Replace full emoji tokens with valid identifiers."""
        import emoji
        result = []
        last_end = 0

        for token in emoji.analyze(code, non_emoji=True, join_emoji=True):
            if isinstance(token.value, emoji.EmojiMatch):
                emoji_char = token.value.emoji
                identifier = self.get_identifier(emoji_char)
                result.append(code[last_end:token.value.start])
                result.append(identifier)
                last_end = token.value.end

        result.append(code[last_end:])
        return ''.join(result)


def run_pymojify_file(file_path, debug=False):
    """Run a pymojify file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    replacer = EmojiReplacer()
    processed_code = replacer.replace_emojis(source_code)

    debug_file = f"{file_path}.debug.py"
    if debug:
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(processed_code)
        print(f"Debug output written to {debug_file}")

    module_name = os.path.basename(file_path).split('.')[0]
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)

    module.__emoji_map__ = replacer.emoji_map
    module.__reverse_map__ = replacer.reverse_map

    try:
        sys.modules[module_name] = module
        exec(processed_code, module.__dict__)
    except Exception as e:
        print(f"Error executing {file_path}:")
        print(e)
        if not debug:  # Always write debug file if there's an error
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(processed_code)
            print(f"(Auto) Debug output written to {debug_file}")
        import traceback
        traceback.print_exc()
    finally:
        if module_name in sys.modules:
            del sys.modules[module_name]



def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="pymojify: Save space and run python with fewer characters using emojis.",
        epilog="Example: python pymojify.py 🌳🖨.🐍 --debug"
    )
    parser.add_argument("file", help="Path to your .🐍 pymojified file")
    parser.add_argument("--de🐛", action="store_true", help="Write the processed .py file for de🐛")


    args = parser.parse_args()
    print(args)

    if not args.file or not args.file.endswith(".🐍"):
        parser.error("The input file must have a .🐍 extension.")

    debug = getattr(args, 'de🐛')
    run_pymojify_file(args.file, debug=debug)


if __name__ == "__main__":
    main()