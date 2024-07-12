from sys import exit
import pygame

pygame.init()

surface = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Chess")

chessboard = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

pieceSelected = False
sourceX, sourceY, destinationX, destinationY = None, None, None, None
possibleMoves = None
playerTurn = 1


class MoveValidator(object):
    def __init__(self):
        self.potentialMoves = []
        self.validatedMoves = []
        self.isWhitePiece = None

    def calculateValidMoves(self, x, y, chessboard):
        global possibleMoves
        self.potentialMoves = []
        self.validatedMoves = []
        self.isWhitePiece = chessboard[x][y].isupper()

        piece = chessboard[x][y].upper()
        if piece == "K":
            possibleMoves = self.kingMoves(x, y, chessboard)
        elif piece == "Q":
            possibleMoves = self.queenMoves(x, y, chessboard)
        elif piece == "R":
            possibleMoves = self.rookMoves(x, y, chessboard)
        elif piece == "B":
            possibleMoves = self.bishopMoves(x, y, chessboard)
        elif piece == "N":
            possibleMoves = self.knightMoves(x, y, chessboard)
        elif piece == "P":
            possibleMoves = self.pawnMoves(x, y, chessboard)
        return possibleMoves

    def kingMoves(self, x, y, chessboard):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                self.potentialMoves.append([x + i, y + j])

        for i in range(len(self.potentialMoves)):
            if (
                self.potentialMoves[i][1] >= 0
                and self.potentialMoves[i][0] >= 0
                and self.potentialMoves[i][1] < 8
                and self.potentialMoves[i][0] < 8
            ):
                base = chessboard[self.potentialMoves[i][0]][self.potentialMoves[i][1]]
                isSameColor = None
                if base == 0:
                    isSameColor = False
                elif self.isWhitePiece:
                    isSameColor = base.isupper()
                else:
                    isSameColor = base.islower()

                if not isSameColor:
                    self.validatedMoves.append([self.potentialMoves[i][0], self.potentialMoves[i][1]])

        return self.validatedMoves

    def queenMoves(self, x, y, chessboard):
        rookResult, bishopResult = self.rookMoves(x, y, chessboard), self.bishopMoves(x, y, chessboard)
        for i in range(len(rookResult)):
            self.potentialMoves.append(rookResult[i])
        for i in range(len(bishopResult)):
            self.potentialMoves.append(bishopResult[i])
        return self.potentialMoves

    def rookMoves(self, x, y, chessboard):
        for i in range(x + 1, 8):
            if chessboard[i][y] == 0:
                self.potentialMoves.append([i, y])
                continue
            if not self.compareColor(i, y, chessboard):
                self.potentialMoves.append([i, y])
                break
            break
        for i in range(x - 1, -1, -1):
            if chessboard[i][y] == 0:
                self.potentialMoves.append([i, y])
                continue
            if not self.compareColor(i, y, chessboard):
                self.potentialMoves.append([i, y])
                break
            break
        for i in range(y + 1, 8):
            if chessboard[x][i] == 0:
                self.potentialMoves.append([x, i])
                continue
            if not self.compareColor(x, i, chessboard):
                self.potentialMoves.append([x, i])
                break
            break
        for i in range(y - 1, -1, -1):
            if chessboard[x][i] == 0:
                self.potentialMoves.append([x, i])
                continue
            if not self.compareColor(x, i, chessboard):
                self.potentialMoves.append([x, i])
                break
            break

        return self.potentialMoves

    def bishopMoves(self, x, y, chessboard):
        for i in range(1, 8):
            if (x + i < 8) and (y + i < 8):
                if chessboard[x + i][y + i] == 0:
                    self.potentialMoves.append([x + i, y + i])
                    continue
                if not self.compareColor(x + i, y + i, chessboard):
                    self.potentialMoves.append([x + i, y + i])
                    break
                break
            else:
                break
        for i in range(1, 8):
            if (x - i >= 0) and (y - i >= 0):
                if chessboard[x - i][y - i] == 0:
                    self.potentialMoves.append([x - i, y - i])
                    continue
                if not self.compareColor(x - i, y - i, chessboard):
                    self.potentialMoves.append([x - i, y - i])
                    break
                break
            else:
                break
        for i in range(1, 8):
            if (x + i < 8) and (y - i >= 0):
                if chessboard[x + i][y - i] == 0:
                    self.potentialMoves.append([x + i, y - i])
                    continue
                if not self.compareColor(x + i, y - i, chessboard):
                    self.potentialMoves.append([x + i, y - i])
                    break
                break
            else:
                break
        for i in range(1, 8):
            if (x - i >= 0) and (y + i < 8):
                if chessboard[x - i][y + i] == 0:
                    self.potentialMoves.append([x - i, y + i])
                    continue
                if not self.compareColor(x - i, y + i, chessboard):
                    self.potentialMoves.append([x - i, y + i])
                    break
                break
            else:
                break

        return self.potentialMoves

    def knightMoves(self, x, y, chessboard):
        if (
            x < 6
            and y < 7
            and (chessboard[x + 2][y + 1] == 0 or not self.compareColor(x + 2, y + 1, chessboard))
        ):
            self.potentialMoves.append([x + 2, y + 1])
        if (
            x < 6
            and y > 0
            and (chessboard[x + 2][y - 1] == 0 or not self.compareColor(x + 2, y - 1, chessboard))
        ):
            self.potentialMoves.append([x + 2, y - 1])
        if (
            x > 1
            and y < 7
            and (chessboard[x - 2][y + 1] == 0 or not self.compareColor(x - 2, y + 1, chessboard))
        ):
            self.potentialMoves.append([x - 2, y + 1])
        if (
            x > 1
            and y > 0
            and (chessboard[x - 2][y - 1] == 0 or not self.compareColor(x - 2, y - 1, chessboard))
        ):
            self.potentialMoves.append([x - 2, y - 1])
        if (
            x < 7
            and y < 6
            and (chessboard[x + 1][y + 2] == 0 or not self.compareColor(x + 1, y + 2, chessboard))
        ):
            self.potentialMoves.append([x + 1, y + 2])
        if (
            x > 0
            and y < 6
            and (chessboard[x - 1][y + 2] == 0 or not self.compareColor(x - 1, y + 2, chessboard))
        ):
            self.potentialMoves.append([x - 1, y + 2])
        if (
            x < 7
            and y > 1
            and (chessboard[x + 1][y - 2] == 0 or not self.compareColor(x + 1, y - 2, chessboard))
        ):
            self.potentialMoves.append([x + 1, y - 2])
        if (
            x > 0
            and y > 1
            and (chessboard[x - 1][y - 2] == 0 or not self.compareColor(x - 1, y - 2, chessboard))
        ):
            self.potentialMoves.append([x - 1, y - 2])
        return self.potentialMoves

    def pawnMoves(self, x, y, chessboard):
        if chessboard[x][y] == "p":
            if x == 1 and chessboard[x + 2][y] == 0:
                self.potentialMoves.append([x + 2, y])
            if chessboard[x + 1][y] == 0:
                self.potentialMoves.append([x + 1, y])
            if (
                y > 0
                and x < 7
                and chessboard[x + 1][y - 1] != 0
                and chessboard[x + 1][y - 1].isupper()
            ):
                self.potentialMoves.append([x + 1, y - 1])
            if (
                y < 7
                and x < 7
                and chessboard[x + 1][y + 1] != 0
                and chessboard[x + 1][y + 1].isupper()
            ):
                self.potentialMoves.append([x + 1, y + 1])
        elif chessboard[x][y] == "P":
            if x == 6 and chessboard[x - 2][y] == 0:
                self.potentialMoves.append([x - 2, y])
            if chessboard[x - 1][y] == 0:
                self.potentialMoves.append([x - 1, y])
            if (
                x > 0
                and y > 0
                and chessboard[x - 1][y - 1] != 0
                and chessboard[x - 1][y - 1].islower()
            ):
                self.potentialMoves.append([x - 1, y - 1])
            if (
                x > 0
                and y < 7
                and chessboard[x - 1][y + 1] != 0
                and chessboard[x - 1][y + 1].islower()
            ):
                self.potentialMoves.append([x - 1, y + 1])

        for i in range(len(self.potentialMoves)):
            if (
                self.potentialMoves[i][1] >= 0
                and self.potentialMoves[i][0] >= 0
                and self.potentialMoves[i][1] < 8
                and self.potentialMoves[i][0] < 8
            ):
                self.validatedMoves.append(self.potentialMoves[i])

        return self.validatedMoves

    def compareColor(self, x, y, chessboard):
        if self.isWhitePiece:
            return chessboard[x][y].isupper()
        else:
            return chessboard[x][y].islower()


moveValidator = MoveValidator()


class ChessboardGraphics(object):
    def __init__(self):
        self.squares = [[], [], [], [], [], [], [], []]
        self.PIECE_IMAGES = [
            pygame.transform.scale(
                pygame.image.load("Assets\\WhiteKing.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\WhiteQueen.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\WhiteRook.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\WhiteBishop.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\WhiteKnight.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\WhitePawn.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackKing.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackQueen.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackRook.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackBishop.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackKnight.png"), (64, 85)
            ),
            pygame.transform.scale(
                pygame.image.load("Assets\\BlackPawn.png"), (64, 85)
            ),
        ]
        self.squareColors = [[], [], [], [], [], [], [], []]
        self.setupChessboard()

    def setupChessboard(self):
        for i in range(8):
            for j in range(8):
                self.squares[i].append(pygame.Rect(j * 80, i * 80, 80, 80))
                if i % 2 == j % 2:
                    self.squareColors[i].append((200, 200, 200))
                else:
                    self.squareColors[i].append((30, 30, 30))

    def drawChessboard(self):
        global surface
        surface.fill((12, 12, 12))
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(surface, self.squareColors[i][j], self.squares[i][j])

    def placeChessPieces(self):
        global surface, chessboard
        for i in range(8):
            for j in range(8):
                if chessboard[i][j] == "K":
                    surface.blit(
                        self.PIECE_IMAGES[0],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[0].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[0].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "Q":
                    surface.blit(
                        self.PIECE_IMAGES[1],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[1].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[1].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "R":
                    surface.blit(
                        self.PIECE_IMAGES[2],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[2].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[2].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "B":
                    surface.blit(
                        self.PIECE_IMAGES[3],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[3].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[3].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "N":
                    surface.blit(
                        self.PIECE_IMAGES[4],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[4].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[4].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "P":
                    surface.blit(
                        self.PIECE_IMAGES[5],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[5].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[5].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "k":
                    surface.blit(
                        self.PIECE_IMAGES[6],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[6].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[6].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "q":
                    surface.blit(
                        self.PIECE_IMAGES[7],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[7].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[7].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "r":
                    surface.blit(
                        self.PIECE_IMAGES[8],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[8].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[8].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "b":
                    surface.blit(
                        self.PIECE_IMAGES[9],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[9].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[9].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "n":
                    surface.blit(
                        self.PIECE_IMAGES[10],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[10].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[10].get_rect().height / 2,
                        ),
                    )
                elif chessboard[i][j] == "p":
                    surface.blit(
                        self.PIECE_IMAGES[11],
                        (
                            self.squares[i][j].x
                            + self.squares[i][j].width / 2
                            - self.PIECE_IMAGES[11].get_rect().width / 2,
                            self.squares[i][j].y
                            + self.squares[i][j].height / 2
                            - self.PIECE_IMAGES[11].get_rect().height / 2,
                        ),
                    )
                elif i % 2 == j % 2:
                    pygame.draw.rect(surface, (200, 200, 200), self.squares[i][j])
                else:
                    pygame.draw.rect(surface, (30, 30, 30), self.squares[i][j])

    def highlightMoves(self, x, y):
        global moveValidator
        self.squareColors[x][y] = (200, 200, 0)
        possibleMoves = moveValidator.calculateValidMoves(x, y, chessboard)
        for i in possibleMoves:
            self.squareColors[i[0]][i[1]] = (255, 121, 164)

    def resetColors(self):
        for i in range(8):
            for j in range(8):
                if i % 2 == j % 2:
                    self.squareColors[i][j] = (200, 200, 200)
                else:
                    self.squareColors[i][j] = (30, 30, 30)


graphics = ChessboardGraphics()


def isValidMove(x1, y1, x2, y2):
    global chessboard, moveValidator
    testBoard = []
    for i in range(8):
        testBoard.append([])
        for j in range(8):
            testBoard[i].append(chessboard[i][j])
    testBoard[x2][y2] = chessboard[x1][y1]
    testBoard[x1][y1] = 0

    isWhite = testBoard[x2][y2].isupper()
    kingPosX, kingPosY = None, None
    opponentPositions = []

    for i in range(8):
        for j in range(8):
            if isWhite:
                if testBoard[i][j] == "K":
                    kingPosX = i
                    kingPosY = j
            else:
                if testBoard[i][j] == "k":
                    kingPosX = i
                    kingPosY = j
            if testBoard[i][j] != 0:
                if isWhite:
                    if testBoard[i][j].islower():
                        opponentPositions.append([i, j])
                else:
                    if testBoard[i][j].isupper():
                        opponentPositions.append([i, j])

    threatMoves = []
    for pos in opponentPositions:
        threatMoves.append(moveValidator.calculateValidMoves(pos[0], pos[1], testBoard))

    for moves in threatMoves:
        for move in moves:
            if kingPosX == move[0] and kingPosY == move[1]:
                return False
    return True


class EventHandler(object):
    def __init__(self):
        self.pieceIsSelected = False
        self.selectedX = None
        self.selectedY = None
        self.destX = None
        self.destY = None
        self.gameTurn = 1

    def handleEvent(self, i, j):
        global chessboard, graphics
        if self.pieceIsSelected:
            self.destX = i
            self.destY = j
            if (
                (
                    self.selectedX != None
                    and self.selectedY != None
                    and self.destX != None
                    and self.destY != None
                )
                and self.selectedX != self.destX
                or self.selectedY != self.destY
            ):
                if isValidMove(
                    self.selectedX, self.selectedY, self.destX, self.destY
                ):
                    self.executeMove(self.selectedX, self.selectedY, self.destX, self.destY)
                else:
                    self.selectedX = None
                    self.selectedY = None
                    self.destX = None
                    self.destY = None
                graphics.drawChessboard()
            else:
                self.selectedX = None
                self.selectedY = None
                self.destX = None
                self.destY = None
                graphics.resetColors()
            graphics.drawChessboard()
            self.pieceIsSelected = False
        else:
            if chessboard[i][j] != 0 and self.checkTurn(i, j):
                self.pieceIsSelected = True
                self.selectedX = i
                self.selectedY = j
                graphics.highlightMoves(self.selectedX, self.selectedY)
                graphics.drawChessboard()
            else:
                self.pieceIsSelected = False
                self.selectedX = None
                self.selectedY = None

    def checkTurn(self, i, j):
        global chessboard
        if self.gameTurn == 1:
            return chessboard[i][j] == 0 or chessboard[i][j].isupper()
        else:
            return chessboard[i][j] == 0 or chessboard[i][j].islower()

    def executeMove(self, x1, y1, x2, y2):
        global chessboard, possibleMoves
        moveValidator.calculateValidMoves(x1, y1, chessboard)
        for move in possibleMoves:
            if move[0] == x2 and move[1] == y2:
                chessboard[x2][y2] = chessboard[x1][y1]
                chessboard[x1][y1] = 0
                self.gameTurn *= -1
                break
        graphics.placeChessPieces()
        graphics.resetColors()


eventController = EventHandler()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        mousePos = pygame.mouse.get_pos()
        for i in range(8):
            for j in range(8):
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and mousePos[0] > graphics.squares[i][j].left
                    and mousePos[1] > graphics.squares[i][j].top
                    and mousePos[0] < graphics.squares[i][j].right
                    and mousePos[1] < graphics.squares[i][j].bottom
                ):
                    eventController.handleEvent(i, j)
    graphics.drawChessboard()
    graphics.placeChessPieces()
    pygame.display.flip()
