# Written by A3therium - 2023
# Made to run AQA's assembly language (with slight adjustments)

from tkinter import filedialog as fd

class CPU:
    def __init__(self) -> None:
        self.regs = [0] * 8
        self.acc = 0
        self.pc = 0
        self.instructions = []
    
    def run(self,file) -> None:
        with open(file,"r") as f:
            self.instructions = f.read().split("\n")

        while self.pc < len(self.instructions):
            lastInst = self.excecute(self.instructions[self.pc])
            self.display(lastInst)
            if lastInst == "HALT": break
            self.pc += 1

    def display(self, instOutput) -> None:
        output = "| Register | Contents (Decimal) |\n"
        for i in range(0,len(self.regs)):
            output += f"|{str(i).center(10)}|{str(self.regs[i]).center(20)}|\n"
        output += f"|{'ACC'.center(10)}|{str(self.acc).center(20)}|\n"
        output += f"|{'PC'.center(10)}|{str(self.pc).center(20)}|\n"
        output += f">>> {instOutput}"
        print("\x1b[H\x1b[0J" + output + "\nPress enter to step\n")
        input()

    def excecute(self,inst) -> str:
        inst = inst.split(",")
        match inst[0]:
            case "//":
                return f"Comment: {inst[1]}"
            case "":
                return ""
            case "VAL":
                return f"Value: {inst[1]}"
            case "LDR":
                mem_loc = self.instructions[int(inst[2])].split(',')
                self.regs[int(inst[1][1:])] = int(mem_loc[1][1:])
                return f"Loaded value {mem_loc[1]} into {inst[1]}"
            case "STR":
                if not self.instructions[int(inst[2])]:
                    mem_loc = self.instructions[inst[2]].split(',')
                else:
                    mem_loc = ["VAL","#0"]
                mem_loc[1] = str(self.regs[int(inst[1][1:])])
                self.instructions[int(inst[2])] = f"{mem_loc[0]},{mem_loc[1]}"
                return f"Stored value {inst[1]} in {inst[2]}"
            case "ADD":
                if inst[3][0] == '#':
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] + int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] + self.regs[int(inst[3][1:])]
                return f"Stored: {inst[2]} + {inst[3]} in {inst[1]}"
            case "SUB":
                if inst[3][0] == '#':
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] - int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] - self.regs[int(inst[3][1:])]
                return f"Stored: {inst[2]} - {inst[3]} in {inst[1]}"
            case "MOV":
                if inst[2][0] == "#":
                    self.regs[int(inst[1][1:])] = int(inst[2][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])]
                return f"Copied: {inst[2]} into {inst[1]}"
            case "CMP":
                num1 = self.regs[int(inst[1][1:])]
                if inst[2][0] == "#":
                    num2 = int(inst[2][1:])
                else:
                    num2 = self.regs[int(inst[2][1:])]
                if num1 == num2: self.acc = 1
                elif num1 > num2: self.acc = 2
                elif num1 < num2: self.acc = 3
                return f"Compared: {inst[1]} against {inst[2]}, result {'equal' if self.acc == 1 else ('greater than' if self.acc == 2 else 'less than')}"
            case "B":
                self.pc = int(inst[1]) - 1
                return f"Branched to: {inst[1]}"
            case "BEQ":
                if self.acc == 1:
                    self.pc = int(inst[1]) - 1
                    return f"Branched to: {inst[1]}"
                else:
                    return f"Did not branch"
            case "BNE":
                if self.acc != 1:
                    self.pc = int(inst[1]) - 1
                    return f"Branched to: {inst[1]}"
                else:
                    return f"Did not branch"
            case "BLT":
                if self.acc == 3:
                    self.pc = int(inst[1]) - 1
                    return f"Branched to: {inst[1]}"
                else:
                    return f"Did not branch"
            case "BGT":
                if self.acc == 2:
                    self.pc = int(inst[1]) - 1
                    return f"Branched to: {inst[1]}"
                else:
                    return f"Did not branch"
            case "AND":
                if inst[3][0] == "#":
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] & int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] & self.regs[int(inst[3][1:])]
                return f"Bitwise AND of: {inst[2]} & {inst[3]}, stored in {inst[1]}"
            case "ORR":
                if inst[3][0] == "#":
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] | int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] | self.regs[int(inst[3][1:])]
                return f"Bitwise OR of: {inst[2]} & {inst[3]}, stored in {inst[1]}"
            case "EOR":
                if inst[3][0] == "#":
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] ^ int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] ^ self.regs[int(inst[3][1:])]
                return f"Bitwise XOR of: {inst[2]} & {inst[3]}, stored in {inst[1]}"
            case "MVN":
                if inst[2][0] == "#":
                    self.regs[int(inst[1][1:])] = ~int(inst[2][1:])
                else:
                    self.regs[int(inst[1][1:])] = ~self.regs[int(inst[2][1:])]
                return f"Bitwise NOT of: {inst[2]}, stored in {inst[1]}"
            case "LSL":
                if inst[3][0] == "#":
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] << int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] << self.regs[int(inst[3][1:])]
                return f"Bitwise shift left: {inst[2]} by {inst[3]}, stored in {inst[1]}"
            case "LSR":
                if inst[3][0] == "#":
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] >> int(inst[3][1:])
                else:
                    self.regs[int(inst[1][1:])] = self.regs[int(inst[2][1:])] >> self.regs[int(inst[3][1:])]
                return f"Bitwise shift right: {inst[2]} by {inst[3]}, stored in {inst[1]}"
            case "HALT":
                return f"HALT"
            case _:
                return f"ERROR: Unkown instruction {inst} on line {self.pc + 1}"

if __name__ == "__main__":
    filename = fd.askopenfilename()
    cpu = CPU()
    cpu.run(filename)
