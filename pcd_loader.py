class PcdLoader:
    def __init__(self, filename: str):
        self.load(filename=filename)

    def _reset(self):
        self.headers = {}
        self.data = {}

    def _build_ascii_header(self) -> str:
        return "\n".join(
            "{} {}".format(key, " ".join(val) if key != "DATA" else "ascii")
            for key, val in self.headers.items()
        )

    def _parse_ascii(self, content):
        lines = [
            line.strip()
            for line in content.decode("utf-8").split("\n")
            if bool(line.strip())
        ]
        self.data = {f: [] for f in self.headers["FIELDS"]}
        for line in lines:
            for v, t, f in zip(
                line.split(" "), self.headers["TYPE"], self.headers["FIELDS"]
            ):
                v = float(v) if t == "F" else int(v)
                self.data[f].append(v)

    def _parse_binary(self, content):
        import struct

        sizes = [int(s) for s in self.headers["SIZE"]]
        self.data = {f: [] for f in self.headers["FIELDS"]}

        def conv_format(t, s):
            if t == "F":
                if s == "4":
                    return "f"
                elif s == "8":
                    return "d"
            elif t in ("I", "U"):
                if s == "1":
                    return "c"
                elif s == "4":
                    return "i"
                elif s == "8":
                    return "q"

            assert 1 == 0, f"unsupported type {t} and size {s}"

        line_format = "".join(
            conv_format(t, s)
            for t, s in zip(self.headers["TYPE"], self.headers["SIZE"])
        )
        num_points = int(self.headers["POINTS"][0])
        content_format = line_format * num_points
        unpacked_struct = struct.unpack(content_format, content)

        ip = 0
        for i in range(num_points):
            for t, f in zip(self.headers["TYPE"], self.headers["FIELDS"]):
                self.data[f].append(unpacked_struct[ip])
                ip += 1

    def save_ascii(self, filename) -> None:
        assert len(set(len(val) for val in self.data.values())) <= 1

        l = len(list(self.data.values())[0]) if bool(self.data) else 0
        with open(filename, "w", encoding="utf-8") as fo:
            fo.write(self._build_ascii_header() + "\n")

            for i in range(l):
                fo.write(
                    " ".join(str(self.data[f][i]) for f in self.headers["FIELDS"])
                    + "\n"
                )

    def load(self, filename: str):
        self._reset()

        with open(filename, "rb") as fi:
            content = fi.read()

        # print(content)
        lines = content.split(b"\n")

        is_header = True
        data_lines = []

        for line in lines:
            if is_header:
                if line.startswith(b"DATA "):
                    is_header = False

                elements = line.decode("utf-8").split(" ")
                self.headers[elements[0]] = elements[1:]
            else:
                data_lines.append(line)

        content = b"\n".join(data_lines)
        self.headers["TYPE"] = [t.upper() for t in self.headers["TYPE"]]
        assert all(t in ("I", "U", "F") for t in self.headers["TYPE"])
        assert all(c == "1" for c in self.headers["COUNT"])

        # print(self.headers)
        # print(self.headers["DATA"])
        if self.headers["DATA"][0] == "ascii":
            self._parse_ascii(content)
        if self.headers["DATA"][0] == "binary":
            self._parse_binary(content)
