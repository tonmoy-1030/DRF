import { Employees } from "@/services/api";

export async function loader({ request }) {
  const url = new URL(request.url);
  const page = url.searchParams.get("page") || 1;
  const response = await Employees(page);
  return {
    employees: response.data.results,
    totalCount: response.data.count,
    currentPage: parseInt(page),
  };
}