class Matrix:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        self.initEmpty()

    def initEmpty(self):
        for i in range(0,self.rows):
            row = []
            for j in range(0,self.cols):
                row.append(0)
            self.data.append(row)

    def dataFromArray(self,array):
        count = 0
        for row in self.data:
            for i in range(0,self.cols):
                row[i] = array[count]
                count += 1

    def transpose(self):
        res = Matrix(self.cols,self.rows)
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                res.data[j][i] = self.data[i][j]
        return res

    def det(self):
        if self.rows != self.cols:
            return 0
        if self.rows == 1 and self.cols == 1:
            return self.data[0][0] 
        determinant = 0
        for i in range(0,self.cols):
            determinant += (-1)**(i) * self.data[0][i] * self.minor(0,i)
        return determinant

    def inverse(self):
        # find determinant
        det = self.det()
        # if det is 0, there's no inverse
        if det == 0:
            return None
        res = Matrix(self.rows,self.cols)
        # matrix of minors with alternating signs
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                res.data[i][j] = (-1)**(i+j) * self.minor(i,j)
        res *= 1/det
        return res.transpose()
        
    def minor(self,row,col):
        tempM = Matrix(self.rows-1,self.cols-1)
        data = []
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                if i != row and j != col:
                    data.append(self.data[i][j])
        tempM.dataFromArray(data)
        return tempM.det()

    def __add__(self,other):
        res = Matrix(self.rows,self.cols)
        if self.rows == other.rows and self.cols == other.cols:
            for i in range(0,self.rows):
                for j in range(0,self.cols):
                    res.data[i][j] = self.data[i][j] + other.data[i][j]
        return res

    def __sub__(self,other):
        self + other*(-1)

    def __mul__(self,other):
        if isinstance(other,Matrix):
            if not(self.cols == other.rows):
                return None
            res = Matrix(self.rows,other.cols)
            for i in range(0,res.rows):
                for j in range(0,res.cols):
                    num = 0
                    for count in range(0,self.cols):
                        num += self.data[i][count]*other.data[count][j]
                    res.data[i][j] = num
            return res
        else:
            for i in range(0,self.rows):
                for j in range(0,self.cols):
                    self.data[i][j] *= other
            return self

    def __eq__(self,other):
        if not(self.rows == other.rows and self.cols == other.cols):
            return False
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    def __repr__(self):
        resStr = ""
        for row in self.data:
            rowStr = ""
            for i in range(0,self.cols):
                rowStr += str(row[i]) + " "
            rowStr += "\n"
            resStr += rowStr
        return resStr