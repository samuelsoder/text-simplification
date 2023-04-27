def find_differences(files):
    while True:
        lines = []
        for file in files:
            lines.append(file.readline())

        if lines[0] == '':
            break
        found = False
        for i in range(len(lines)):
            line = lines[i]
            for l in lines[i + 1:]:
                if line == l:
                    found = True
        if not found:
            print(lines)
        found = False


def main():
    files = [
        open('out/simplified/asset.sv.test.orig.simplified.mined'),
        open('out/simplified/asset.sv.test.orig.simplified.fully.mined'),
        open('out/simplified/asset.sv.test.orig.simplified.translated'),
        open('out/simplified/asset.sv.test.orig.simplified.fully.translated'),
        open('out/simplified/asset.sv.test.orig.simplified.combined'),
        open('out/simplified/asset.sv.test.orig.simplified.fully.combined'),
    ]
    'Han har också blivit utsedd till Årets idrottsman av Sports Illustrated.\n'
    'Han har också blivit utsedd till Årets Idrottsman av Sports Illustrated.\n'
    find_differences(files)


if __name__ == '__main__':
    main()