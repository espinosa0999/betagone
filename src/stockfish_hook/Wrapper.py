import chess
import chess.engine

class Wrapper:
    def __init__(self, engine_path:str, thinktime:float=2.0):
        self.engine_path = engine_path

        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.board = None
        self.thinktime = thinktime

    def process_position(self, fen) -> chess.Move:
        self.board = chess.Board(fen)
        move = self.engine.play(self.board, chess.engine.Limit(time=self.thinktime))

        return move.move

    def translate_move(self, move:chess.Move) -> str:
        """
        Converteix la representacio de la jugada en un format indepentent de
        context per simplificar el modul de control i minimitzar l'acoblament

        La representacio es la seguent:
            <columna_origen> <fila_origen> <columna_desti> <fila_desti> [<opt>]
        Aquests numeros van de 0 a 7 respectivament
        Els opcionals <opt> poden ser:
            -> Captura: x <simbol_peça> (e <columna_alpas> <fila_alpas>)
            -> Promocio: = <simbol_peça>

        Parameters
        ----------
        move

        Returns
        -------

        """
        string_move = str(move)
        ret_move = ""
        for ch in string_move[0:4]:
            ret_move += str(ord(ch) - ord('a')) if ch in "abcdefgh" else str(int(ch)-1)
        ret_move += "["
        if self.board.is_capture(move):
            ret_move += 'x'
            piece = chess.piece_symbol(self.board.piece_type_at(chess.square(int(ret_move[2]), int(ret_move[3]))))
            ret_move += piece.upper() if self.board.turn == chess.BLACK else piece.lower()
            if self.board.is_en_passant(move):
                ret_move += ""
                if self.board.turn == chess.WHITE:
                    ret_move += ret_move[2] + str(int(ret_move[3]) - 1)
                else:
                    ret_move += ret_move[2] + str(int(ret_move[3]) + 1)
        if len(string_move) == 5:
            ret_move += "=" + string_move[-1].upper() if self.board.turn == chess.BLACK else string_move[-1].lower()
        ret_move += "]"

        return ret_move

    def shutdown(self):
        self.engine.quit()