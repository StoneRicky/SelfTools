package cn.mdk.common.utils.pdf;

import com.itextpdf.kernel.colors.DeviceRgb;
import com.itextpdf.kernel.events.PdfDocumentEvent;
import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.borders.Border;
import com.itextpdf.layout.element.AreaBreak;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.properties.AreaBreakType;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;
import com.itextpdf.layout.properties.VerticalAlignment;
import org.apache.poi.hssf.usermodel.HSSFCellStyle;
import org.apache.poi.hssf.usermodel.HSSFFont;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.usermodel.XSSFCellStyle;
import org.apache.poi.xssf.usermodel.XSSFFont;
import org.springframework.beans.factory.annotation.Value;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

/**
 * @author fengxxc
 * @date 2022-12-05
 */
public class Excel2PDF {


    public static String DEFAULT_FONT_PATH = ITextUtil.DEFAULT_FONT;



    public Excel2PDF() throws IOException {
    }

    /**
     * Excel 转 PDF
     * @param is Excel文件 输入流
     * @param os PDF文件 输出流
     * @throws IOException
     */
    public static void process(InputStream is, OutputStream os) throws IOException {
        process(is, os, null, null, null);
    }

    /**
     * Excel 转 PDF
     * @param is Excel文件 输入流
     * @param os PDF文件 输出流
     * @param documentCallback document建立后的回调函数
     * @throws IOException
     */
    public static void process(InputStream is, OutputStream os, Consumer<Document> documentCallback) throws IOException {
        process(is, os, null, documentCallback);
    }

    /**
     * Excel 转 PDF
     * @param is Excel文件 输入流
     * @param os PDF文件 输出流
     * @param documentCallback document建立后的回调函数
     * @param documentCallback document建立后的回调函数
     * @throws IOException
     */
    public static void process(InputStream is, OutputStream os, Consumer<Document> documentCallback, Consumer<E2pPageEvent> pageStartedCallback) throws IOException {
        final Workbook workbook = WorkbookFactory.create(is);
        process(workbook, os, null, documentCallback, pageStartedCallback);
    }

    /**
     * Excel 转 PDF
     * @param is Excel文件 输入流
     * @param os PDF文件 输出流
     * @param columnWidthsArray 每个页的PDF表格列宽
     * @param documentCallback document建立后的回调函数
     * @throws IOException
     */
    public static void process(InputStream is, OutputStream os, UnitValue[][] columnWidthsArray, Consumer<Document> documentCallback) throws IOException {
        final Workbook workbook = WorkbookFactory.create(is);
        process(workbook, os, columnWidthsArray, documentCallback, null);
    }

    /**
     * Excel 转 PDF
     * @param is Excel文件 输入流
     * @param os PDF文件 输出流
     * @param columnWidthsArray 每个页的PDF表格列宽
     * @param documentCallback document建立后的回调函数
     * @param pageStartedCallback page建立后的回调函数
     * @throws IOException
     */
    public static void process(InputStream is, OutputStream os, UnitValue[][] columnWidthsArray, Consumer<Document> documentCallback, Consumer<E2pPageEvent> pageStartedCallback) throws IOException {
        final Workbook workbook = WorkbookFactory.create(is);
        process(workbook, os, columnWidthsArray, documentCallback, pageStartedCallback);
    }

    /**
     * Excel 转 PDF
     * @param workbook POI Workbook 对象
     * @param os PDF文件 输出流
     * @throws IOException
     */
    public static void process(Workbook workbook, OutputStream os) throws IOException {
        process(workbook, os, null, null, null);
    }

    /**
     * Excel 转 PDF
     * @param workbook POI Workbook 对象
     * @param os PDF文件 输出流
     * @param documentCallback document建立后的回调函数
     * @throws IOException
     */
    public static void process(Workbook workbook, OutputStream os, Consumer<Document> documentCallback) throws IOException {
        process(workbook, os, null, documentCallback, null);
    }

    /**
     * Excel 转 PDF
     * @param workbook POI Workbook 对象
     * @param os PDF文件 输出流
     * @param documentCallback document建立后的回调函数
     * @param pageStartedCallback page建立后的回调函数
     * @throws IOException
     */
    public static void process(Workbook workbook, OutputStream os, Consumer<Document> documentCallback, Consumer<E2pPageEvent> pageStartedCallback) throws IOException {
        process(workbook, os, null, documentCallback, pageStartedCallback);
    }

    /**
     * Excel 转 PDF
     *
     * @param workbook          POI Workbook 对象
     * @param os                PDF文件 输出流
     * @param columnWidthsArray 每个页的PDF表格列宽
     * @param documentCallback  document建立后的回调函数
     * @param pageStartedCallback
     * @throws IOException
     */
    private static void process(Workbook workbook, OutputStream os, UnitValue[][] columnWidthsArray, Consumer<Document> documentCallback, Consumer<E2pPageEvent> pageStartedCallback) throws IOException {
        Map<String, PdfFont> fontCache = new HashMap<String, PdfFont>() {{
//            ITextUtil.setDefaultFont();
            System.out.println(DEFAULT_FONT_PATH);
            put(DEFAULT_FONT_PATH, ITextUtil.createFont(DEFAULT_FONT_PATH));
        }};

        // init pdf document
        final PdfWriter pdfWriter = new PdfWriter(os);
        final PdfDocument pdfDocument = new PdfDocument(pdfWriter);
        PdfPageEventHandler pdfPageEventHandler = new PdfPageEventHandler(pageStartedCallback);
        pdfDocument.addEventHandler(PdfDocumentEvent.START_PAGE, pdfPageEventHandler);
        final Document document = new Document(pdfDocument);
        document.setFont(fontCache.get(DEFAULT_FONT_PATH));
        if (documentCallback != null) {
            documentCallback.accept(document);
        }

        // final XSSFWorkbook workbook = new XSSFWorkbook(is);
        for (int sheetIdx = 0; sheetIdx < workbook.getNumberOfSheets(); sheetIdx++) {
            final Sheet sheet = workbook.getSheetAt(sheetIdx);
            pdfPageEventHandler.setSheetAt(sheetIdx);
            pdfPageEventHandler.setSheetName(sheet.getSheetName());
            if (sheetIdx > 0) {
                // 下一页
                document.add(new AreaBreak(AreaBreakType.NEXT_PAGE));
            }
            UnitValue[] columnWidths = null;
            if (columnWidthsArray != null && sheetIdx < columnWidthsArray.length) {
                columnWidths = columnWidthsArray[sheetIdx];
            }
            renderSheet(columnWidths, document, sheet, null);
        }

        document.close();
    }

    /**
     * 渲染一个sheet的内容为表格输出到PDF的document中
     * @param columnWidths PDF表格列宽，为null则自动计算
     * @param document PDF的document
     * @param sheet Excel的sheet
     * @param fontCache
     * @throws IOException
     */
    private static void renderSheet(UnitValue[] columnWidths, Document document, Sheet sheet, Map<String, PdfFont> fontCache) throws IOException {
        final Workbook workbook = sheet.getWorkbook();
        if (columnWidths == null) {
            // 如果columnWidths为null，则自动计算列宽
            columnWidths = ExcelUtil.findMaxRowColWidths(sheet);
        }
        if (columnWidths.length == 0) {
            // 如果没有列宽，则直接返回
            return;
        }
        // 创建一个表格
        final Table table = new Table(columnWidths, false);
        // 设置表格宽度为100%
        table.setWidth(new UnitValue(UnitValue.PERCENT, 100)).setVerticalAlignment(VerticalAlignment.MIDDLE);

        // 获取合并单元格列表
        final List<CellRangeAddress> combineCellList = ExcelUtil.getCombineCellList(sheet);
        for (Row row : sheet) {
            // 如果整行都为空，且不是零高度，则插入空单元格
            if (row.getPhysicalNumberOfCells() == 0 && !row.getZeroHeight()) {
                // full row was null
                final float height = row.getHeightInPoints();
                for (int i = 0; i < columnWidths.length; i++) {
                    final com.itextpdf.layout.element.Cell cellNull = ITextUtil.cellNull();
                    cellNull.setHeight(height);
                    // 设置空单元格样式
                    setPdfTableNullCellStyle(sheet, row.getRowNum(), i, cellNull);
                    table.addCell(cellNull);
                }
            }
            int colIdx = 0;

            for (Cell cell : row) {
                // type
                final CellType cellType = cell.getCellType();
                // value
                final String value = ExcelUtil.getCellValue(workbook, cell);
                // style
                final CellStyle cellStyle = cell.getCellStyle();
                // cell width
                final int columnWidth = sheet.getColumnWidth(cell.getColumnIndex());
                // 判断是否合并单元格
                final CellRangeAddress cellRangeAddress = ExcelUtil.getCombineCellRangeAddress(combineCellList, cell);
                final boolean isCombineCell = cellRangeAddress != null ? true : false;
                final boolean isFirstInCombineCell = ExcelUtil.isFirstInCombineCell(cellRangeAddress, cell);

                // to pdf
                // 补充空单元格 导致多空行，暂时注释
//                for (int i = 0; i < cell.getColumnIndex() - colIdx; i++) {
//                    final com.itextpdf.layout.element.Cell cellNull = ITextUtil.cellNull();
//                    int a = row.getRowNum();
//                    // 设置空单元格样式
//                    setPdfTableNullCellStyle(sheet, row.getRowNum(), colIdx + i, cellNull);
//                    table.addCell(cellNull);
//                }
                // 高
                int rowSpan = 1;
                // 宽
                int colSpan = 1;

                // 如果是合并单元格，则设置合并单元格的宽高
                if (isFirstInCombineCell) {
                    rowSpan = cellRangeAddress.getLastRow() - cellRangeAddress.getFirstRow() + 1;
                    colSpan = cellRangeAddress.getLastColumn() - cellRangeAddress.getFirstColumn() + 1;
                }


                com.itextpdf.layout.element.Cell pdfCell = new com.itextpdf.layout.element.Cell();
                // 设置位置
                pdfCell.setFixedPosition(cell.getColumnIndex()+ 1,cell.getRowIndex() + 1 ,columnWidth);
                //设置字体
                pdfCell = ITextUtil.cell(rowSpan, colSpan, value, ITextUtil.createFont(DEFAULT_FONT_PATH));

                // 设置样式
                setPdfTableCellStyle(workbook, cell, pdfCell);
                if (!isCombineCell || isFirstInCombineCell) {
                    table.addCell(pdfCell);
                }
                colIdx = cell.getColumnIndex() + 1;
            }
            // 添加新行 疑似无用
                table.startNewRow();


        }

//        // render picture
//        final Drawing<?> drawingPatriarch = sheet.createDrawingPatriarch();
//        List<? extends Shape> shapes = new ArrayList<>();
//        final HashMap<Position, Picture> pos2picture = new HashMap<>();
//        if (drawingPatriarch instanceof XSSFDrawing) {
//            shapes = ((XSSFDrawing) drawingPatriarch).getShapes();
//        } else if (drawingPatriarch instanceof HSSFPatriarch) {
//            shapes = ((HSSFPatriarch) drawingPatriarch).getChildren();
//        }
//        for (Shape shape : shapes) {
//            Picture picture = null;
//            if (shape instanceof HSSFPicture) {
//                picture = ((HSSFPicture) shape);
//            } else if (shape instanceof XSSFPicture) {
//                picture = ((XSSFPicture) shape);
//            } else {
//                continue;
//            }
//            final ClientAnchor clientAnchor = picture.getClientAnchor();
//            // final int row = clientAnchor.getRow1();
//            // 在合并单元格中，poi认为内容单元格是左上角的单元格，而itext认为是左下角的单元格，所以取row2
//            final int row = clientAnchor.getRow2();
//            final Position pos = new Position(clientAnchor.getCol1(), row);
//            pos2picture.put(pos, picture);
//        }
//        // 设置表格渲染器
//        table.setNextRenderer(new PdfTableRenderer<>(table, pos2picture));

        // 将表格添加到document中
        document.add(table);
    }

    private static PdfFont getFont(Map<String, PdfFont> fontCache, String fontPath) throws IOException {
        PdfFont font = fontCache.get(fontPath);
        if (font == null) {
            font = ITextUtil.createFont(fontPath);
            fontCache.put(fontPath, font);
        }
        return font;
    }

    private static String getFontPath(Workbook workbook, CellStyle cellStyle) {
        String fontPath = null;
        String fontName = null;
        if (cellStyle instanceof XSSFCellStyle) {
            final XSSFFont xssfFont = ((XSSFCellStyle) cellStyle).getFont();
            fontName = xssfFont.getFontName();
        } else if (cellStyle instanceof HSSFCellStyle) {
            final HSSFFont hssfFont = ((HSSFCellStyle) cellStyle).getFont(workbook);
            fontName = hssfFont.getFontName();
        }
//        switch (fontName) {
//            case "宋体":
//                fontPath = ITextUtil.FONT_SIMSUN;
//                break;
//            case "Arial":
//            case "Times New Roman":
//            case "等线":
//                fontPath = ITextUtil.FONT_DENGXIAN;
//                break;
//            case "黑体":
//                fontPath = ITextUtil.FONT_SIMHEI;
//                break;
//            default:
//                fontPath = ITextUtil.FONT_SIMSUN;
//        }
        return fontPath;
    }

    private static void setPdfTableNullCellStyle(Sheet sheet, int rowIndex, int colIndex, com.itextpdf.layout.element.Cell pdfCell) {
        // border style
        // 获取上方单元格
        final Cell aboveCell = ExcelUtil.getAboveCell(rowIndex, colIndex, sheet);
        // 如果上方单元格不为空
        if (aboveCell != null) {
            // 获取上方单元格的底部边框样式
            final BorderStyle aboveBorderBottom = aboveCell.getCellStyle().getBorderBottom();
            // 如果上方单元格的底部边框样式不为空
            if (aboveBorderBottom != BorderStyle.NONE) {
                // 设置pdfCell的顶部边框样式为上方单元格的底部边框样式
                pdfCell.setBorderTop(ITextUtil.POI_TO_ITEXT_BORDER.get(aboveBorderBottom.getCode()));
            } else {
                // 否则，设置pdfCell的顶部边框样式为无边框
                pdfCell.setBorderTop(Border.NO_BORDER);
            }
        } else {
            // 如果上方单元格为空，设置pdfCell的顶部边框样式为无边框
            pdfCell.setBorderTop(Border.NO_BORDER);
        }

        // 设置pdfCell的右侧边框样式为无边框
        pdfCell.setBorderRight(Border.NO_BORDER);
        // 设置pdfCell的底部边框样式为无边框
        pdfCell.setBorderBottom(Border.NO_BORDER);
        // 设置pdfCell的左侧边框样式为无边框
        pdfCell.setBorderLeft(Border.NO_BORDER);
    }

    private static void setPdfTableCellStyle(Workbook workbook, Cell cell, com.itextpdf.layout.element.Cell pdfCell) {
        CellStyle cellStyle = cell.getCellStyle();
        // border style
        final Cell aboveCell = ExcelUtil.getAboveCell(cell);
        final BorderStyle borderTop = cellStyle.getBorderTop();
        if (aboveCell != null) {
            final BorderStyle aboveBorderBottom = aboveCell.getCellStyle().getBorderBottom();
            if (aboveBorderBottom != BorderStyle.NONE && borderTop == BorderStyle.NONE) {
                pdfCell.setBorderTop(ITextUtil.POI_TO_ITEXT_BORDER.get(aboveBorderBottom.getCode()));
            } else if (aboveBorderBottom == BorderStyle.NONE && borderTop != BorderStyle.NONE) {
                pdfCell.setBorderTop(ITextUtil.POI_TO_ITEXT_BORDER.get(borderTop.getCode()));
            } else if (aboveBorderBottom != BorderStyle.NONE && borderTop != BorderStyle.NONE) {
                pdfCell.setBorderTop(ITextUtil.POI_TO_ITEXT_BORDER.get(borderTop.getCode()));
            } else {
                pdfCell.setBorderTop(Border.NO_BORDER);
            }
        } else {
            pdfCell.setBorderTop(ITextUtil.POI_TO_ITEXT_BORDER.get(borderTop.getCode()));
        }

        pdfCell.setBorderRight(ITextUtil.POI_TO_ITEXT_BORDER.get(cellStyle.getBorderRight().getCode()));
        pdfCell.setBorderBottom(ITextUtil.POI_TO_ITEXT_BORDER.get(cellStyle.getBorderBottom().getCode()));

        final Cell leftCell = ExcelUtil.getLeftCell(cell);
        final BorderStyle borderLeft = cellStyle.getBorderLeft();
        if (leftCell != null) {
            final BorderStyle leftBorderRight = leftCell.getCellStyle().getBorderRight();
            if (leftBorderRight != BorderStyle.NONE && borderLeft == BorderStyle.NONE) {
                pdfCell.setBorderLeft(ITextUtil.POI_TO_ITEXT_BORDER.get(leftBorderRight.getCode()));
            } else if (leftBorderRight == BorderStyle.NONE && borderLeft != BorderStyle.NONE) {
                pdfCell.setBorderLeft(ITextUtil.POI_TO_ITEXT_BORDER.get(borderLeft.getCode()));
            } else if (leftBorderRight != BorderStyle.NONE && borderLeft != BorderStyle.NONE) {
                pdfCell.setBorderLeft(ITextUtil.POI_TO_ITEXT_BORDER.get(borderLeft.getCode()));
            } else {
                pdfCell.setBorderLeft(Border.NO_BORDER);
            }
        } else {
            pdfCell.setBorderLeft(ITextUtil.POI_TO_ITEXT_BORDER.get(borderLeft.getCode()));
        }

        // background color
        final Color fillForegroundColorColor = cellStyle.getFillForegroundColorColor();
        final int[] colorARGB = ExcelUtil.getColorARGB(fillForegroundColorColor);
        if (colorARGB != null) {
            pdfCell.setBackgroundColor(new DeviceRgb(colorARGB[1], colorARGB[2], colorARGB[3]));
        }

        // does font bold
        final int fontIndex = cellStyle.getFontIndexAsInt();
        final Font font = workbook.getFontAt(fontIndex);
        final boolean bold = font.getBold();
        if (bold) {
            pdfCell.setBold();
        }

        // font color
        final int[] fontColorRGB = ExcelUtil.getFontColorARGB(font, workbook);
        if (fontColorRGB != null) {
            pdfCell.setFontColor(new DeviceRgb(fontColorRGB[1], fontColorRGB[2], fontColorRGB[3]));
        }


        // font size
        final short fontHeightInPoints = font.getFontHeightInPoints();
        pdfCell.setFontSize(fontHeightInPoints);

        // text align
        final HorizontalAlignment alignment = cellStyle.getAlignment();
        switch (alignment) {
            case FILL:
            case JUSTIFY:
                pdfCell.setTextAlignment(TextAlignment.JUSTIFIED);
                break;
            case RIGHT:
                pdfCell.setTextAlignment(TextAlignment.RIGHT);
                break;
            case CENTER:
            case CENTER_SELECTION:
                pdfCell.setTextAlignment(TextAlignment.CENTER);
                break;
            case LEFT:
            case GENERAL:
                pdfCell.setTextAlignment(TextAlignment.LEFT);
                break;
            case DISTRIBUTED:
                pdfCell.setTextAlignment(TextAlignment.JUSTIFIED_ALL);
                break;
            default:
        }

        // vertical align
        final org.apache.poi.ss.usermodel.VerticalAlignment verticalAlignment = cellStyle.getVerticalAlignment();
        switch (verticalAlignment) {
            case DISTRIBUTED:
            case CENTER:
            case JUSTIFY:
                pdfCell.setVerticalAlignment(VerticalAlignment.MIDDLE);
                break;
            case TOP:
                pdfCell.setVerticalAlignment(VerticalAlignment.TOP);
                break;
            case BOTTOM:
                pdfCell.setVerticalAlignment(VerticalAlignment.BOTTOM);
                break;
            default:
        }
    }
}